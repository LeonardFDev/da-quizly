from django.urls import path, include
from rest_framework import routers

from .views import QuizzeViewSet


router = routers.SimpleRouter()
router.register(r"quizzes", QuizzeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]