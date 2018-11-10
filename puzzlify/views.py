from django.shortcuts import redirect, render

# Create your views here.
from django.http import HttpResponse


def start_puzzle(request, puzzle):
    return HttpResponse("Hello, world. You're at the polls index. {}".format(puzzle))


def question(request, puzzle, question):
    answer = None
    if request.method == "POST":
        answer = request.POST["answer"]
        # TODO: validate answer
        if answer == "yes":
            return redirect('question', puzzle=puzzle, question=question + "-next")

    context = {
        'puzzle': puzzle,
        'question': question,
        'hint': "This is a hint!",
        'answer': answer,
    }
    return render(request, 'question.html', context)
