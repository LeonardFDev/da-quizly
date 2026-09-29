from rest_framework.viewsets import ModelViewSet

from quiz_management_app.models import Quiz
from .serializers import QuizzeSerializer
from .permissions import QuizPermission


class QuizzeViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizzeSerializer

    permission_classes = [QuizPermission]
    http_method_names = ["get", "post", "patch", "delete"]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)

    def get_queryset(self):
        if self.action == "list":
            return Quiz.objects.filter(owner=self.request.user)
        return Quiz.objects.all()