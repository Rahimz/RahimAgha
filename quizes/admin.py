from django.contrib import admin

from .models import Quiz, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'difficulty', 'uses', 'correct_responses']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'difficulty', 'result', 'completed']
