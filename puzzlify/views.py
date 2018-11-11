from django.shortcuts import redirect, render

from django.http import Http404, HttpResponse

from .models import Puzzle, Question


def start_puzzle(request, puzzle_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)

    # TODO: add short explanation of rules, show description, and button that redirects
    # to first question
    if not puzzle.first_question:
        raise Http404
    return redirect('question', puzzle_id=puzzle.id, question_id=puzzle.first_question.id)


def end_puzzle(request, puzzle_id, end_uuid):
    puzzle = Puzzle.objects.get(id=puzzle_id, end_uuid=end_uuid)
    return HttpResponse(puzzle.end_message)


def question(request, puzzle_id, question_id):
    puzzle = Puzzle.objects.get(id=puzzle_id)
    question = Question.objects.get(id=question_id)

    if request.method == "POST":
        answer = request.POST["answer"]
        if question.has_valid_answer(answer):
            if question.next_question:
                return redirect('question', puzzle_id=puzzle.id, question_id=question.next_question.id)
            else:
                # TODO: redirect to win?
                return redirect('question', puzzle_id=puzzle.id, question_id=puzzle.first_question.id)
        else:
            # TODO: show "incorrect answer"
            pass

    context = {
        'puzzle': puzzle,
        'question': question,
        'hint': "This is a hint!",
        # 'answer': answer,
    }
    return render(request, 'question.html', context)
