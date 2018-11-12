import uuid

from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Puzzle(models.Model):
    """A puzzle is a set of one or more questions."""

    id = models.SlugField(primary_key=True, blank=False, max_length=32,
                          help_text="Use something nice, this will be part of visible URLs")

    name = models.CharField(unique=True, blank=False, max_length=30,
                            help_text="A short name to display to users")

    # Defines the start of the puzzle
    start_message = models.TextField(blank=False,
                                     help_text="The message to display at the start of the puzzle.")
    first_question = models.ForeignKey(
        'Question', on_delete=models.SET_NULL, blank=True, null=True, related_name='+',
        help_text="What should be the first question to start this puzzle? If not set, the puzzle can't be played. " +
        "Okay to come back and set this field later.")

    # Defines the end of the puzzle.
    end_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    end_message = models.TextField(
        blank=True,
        help_text="The message to display at the end of the puzzle, upon successful completion. " +
        "The puzzle end is reached when the user encouters a Question without a next_question field!")

    def __str__(self):
        return 'Puzzle: {}'.format(self.name)

    def get_absolute_url(self):
        return reverse('start_puzzle', args=[self.id])

    ###
    # Admin view
    ###
    def html_link(self):
        url = self.get_absolute_url()
        return format_html(
            '<a href="{}" target="_blank">{}</a>', url, url)
    html_link.short_description = 'View on site'


class Question(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Defines position in the puzzle.
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    next_question = models.ForeignKey(
        'Question', on_delete=models.PROTECT, blank=True, null=True, related_name='+',
        help_text="If answered correctly, what should the next question be? " +
        "Okay to come back and set this field later.")

    name = models.CharField(unique=True, blank=False, max_length=30,
                            help_text="A short name to display to users")
    question = models.TextField(
        help_text="A question, challenge or hint that the user must answer. E.g. 'What's the first number?'")
    answers = models.CharField(
        max_length=200,
        help_text="One or more valid answers, separated by commas. E.g. 'one,zero,1'")

    def __str__(self):
        return 'Question:{}, from {}'.format(self.name, self.puzzle)

    def has_valid_answer(self, answer):
        # TODO: could be improved by using some sort of CommaSeparatedListField
        def normalize(s): return s.strip().lower()
        valid_answers = set(normalize(s) for s in self.answers.split(","))
        answer = normalize(answer)
        return answer in valid_answers

    def get_absolute_url(self):
        return reverse('question', args=[self.puzzle.id, self.id])

    ###
    # Admin view
    ###
    def position_in_puzzle(self):
        if not self.puzzle.first_question:
            return "(puzzle has no first_question)"
        index = 0
        head = self.puzzle.first_question
        while head:
            index += 1
            if head == self:
                if self.next_question is None:
                    return "#{} | last question".format(index)
                else:
                    return "#{}".format(index)
            head = head.next_question
        return "(not reachable from first_question)"
    position_in_puzzle.short_description = 'Position in puzzle'

    def html_link(self):
        url = self.get_absolute_url()
        return format_html(
            '<a href="{}" target="_blank">{}</a>', url, url)
    html_link.short_description = 'View on site'
