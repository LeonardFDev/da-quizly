"""URL configuration for the quizzes API."""

from django.urls import path, include
from rest_framework import routers

from .views import QuizViewSet


router = routers.SimpleRouter()
router.register(r"quizzes", QuizViewSet)

urlpatterns = [
    path("", include(router.urls)),
]