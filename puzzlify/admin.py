from django.contrib import admin

from .models import Puzzle, Question


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'html_link')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'position_in_puzzle', 'html_link')


admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(Question, QuestionAdmin)
