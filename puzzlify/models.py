import uuid

from django.db import models
from django.urls import reverse


class Puzzle(models.Model):
    """A puzzle is a set of one or more questions."""

    # TODOs:
    #  * add background image for the entire puzzle
    #  * can we include links?
    #  * what about the last question? what if it should include a link, or different image?
    #  * maybe generate shorter UUID links for the questions?

    id = models.SlugField(primary_key=True, blank=False, max_length=32,
                          help_text="Use something nice, this will be part of visible URLs")

    name = models.CharField(unique=True, blank=False, max_length=30,
                            help_text="A short name to display to users")
    description = models.CharField(blank=False, max_length=500)

    # Defines the start of the puzzle
    first_question = models.ForeignKey(
        'Question', on_delete=models.SET_NULL, blank=True, null=True, related_name='+',
        help_text="What should be the first question to start this puzzle? If not set, the puzzle can't be played. " +
        "Okay to come back and set this field later.")

    # Defines the end of the puzzle.
    end_message = models.TextField(
        blank=True,
        help_text="The message to display at the end of the puzzle, upon successful completion. " +
        "The puzzle end is reached when the user encouters a Question without a next_question field!")

    def __str__(self):
        return 'Puzzle: {}'.format(self.name)

    def get_absolute_url(self):
        return reverse('start_puzzle', args=[self.id])


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
    question = models.TextField()
    answer = models.CharField(max_length=50)

    def __str__(self):
        return 'Question:{}, from {}'.format(self.name, self.puzzle)

    def get_absolute_url(self):
        return reverse('question', args=[self.puzzle.id, self.id])
