"""quizzes views."""

from rest_framework.viewsets import ModelViewSet

from quiz_management_app.models import Quiz
from .serializers import QuizSerializer
from .permissions import QuizPermission


class QuizViewSet(ModelViewSet):
    """Provides API endpoints for managing quizzes."""
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    permission_classes = [QuizPermission]
    http_method_names = ["get", "post", "patch", "delete"]
    
    def perform_create(self, serializer):
        """Create a quiz and hand over the logged in user as the owner."""
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        """At list, only the quizzes in which the login user is the owner will be issued"""
        if self.action == "list":
            return Quiz.objects.filter(owner=self.request.user)
        return Quiz.objects.all()