from django.shortcuts import redirect, render

from django.http import Http404, HttpResponse

from .models import Puzzle, Question


def start_puzzle(request, puzzle_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    if not puzzle.first_question:
        raise ValueError(
            "Puzzle {} does not have a first_question defined".format(puzzle))

    return render(request, 'start.html', context=dict(puzzle=puzzle))


def end_puzzle(request, puzzle_id, end_uuid):
    puzzle = Puzzle.objects.get(id=puzzle_id, end_uuid=end_uuid)
    return render(request, 'end.html', context=dict(puzzle=puzzle))


def question(request, puzzle_id, question_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    question = Question.objects.get(id=question_id)

    answer = None
    if request.method == "POST":
        answer = request.POST["answer"]
        if question.has_valid_answer(answer):
            if question.next_question:
                return redirect('question', puzzle_id=puzzle.id, question_id=question.next_question.id)
            else:
                return redirect('end_puzzle', puzzle_id=puzzle.id, end_uuid=puzzle.end_uuid)
        # Will display annswer as "incorrect".

    return render(request, 'question.html', dict(puzzle=puzzle, question=question, answer=answer))
