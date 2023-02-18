from django.contrib import admin

from .models import Quiz, Question, QuizResponse, Compliment


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'difficulty', 'uses', 'correct_responses']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'difficulty', 'final_result', 'completed', 'ip', 'created']


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'quiz', 'question', 'correct_answer', 'user_response']


@admin.register(Compliment)
class ComplimentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'difficulty']
