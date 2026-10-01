"""Admin configurations for quiz and question"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.html import format_html
from .models import Quiz, Question


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin configuration for the quiz model."""

    list_display = ("id", "title", "video_url", "owner", "quiz_question")
    ordering = ["id"]
    search_fields = ("title", "owner__username", "quiz_question__question_title", "quiz_question__question_options")

    @admin.display(description="Questions")
    def quiz_question(self, obj):
        """Returns the questions as a link displayed in the admin list."""
        def questions_link(quiz_question):
            """Generate the URL and pass the URL, the question title, and the question ID"""
            url = reverse("admin:quiz_management_app_question_change", args=[quiz_question.id])
            return url, quiz_question.question_title, quiz_question.id

        return format_html_join(", ", "[<a href='{}''>{} ({})</a>]",
            (questions_link(quiz_question) for quiz_question in obj.quiz_question.all().order_by("id"))
        )
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin configuration for the question model."""

    list_display = ("id", "question_title", "question_options", "custom_quiz", )
    ordering = ["id"]
    search_fields = ("question_title", "quiz__title", "quiz__description")

    @admin.display(description="Quiz")
    def custom_quiz(self, obj):
        """Returns the quiz as a link displayed in the admin list."""
        quiz = obj.quiz
        url = reverse("admin:quiz_management_app_quiz_change", args=[quiz.id])
        path = "<a href='{}'>{} ({})</a>"
    
        return format_html(path, url, quiz.title, quiz.id)