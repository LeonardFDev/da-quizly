from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    """Represents a quiz of the application."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_url = models.CharField(max_length=200)

    def __str__(self):
        """Return the title and the id as a string."""
        return f"{self.title} ({self.id})"


class Question(models.Model):
    """Represents a question detail of the application."""

    question_title = models.CharField(max_length=100)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="quiz_question")

    def __str__(self):
        """Return the question title and the id as a string."""
        return f"{self.question_title} ({self.id})"
