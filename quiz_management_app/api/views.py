from rest_framework.viewsets import ModelViewSet

from quiz_management_app.models import Quiz, Question
from .serializers import QuizzeSerializer
# from .permissions import 


class QuizzeViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizzeSerializer

    # permission_classes = []
    http_method_names = ["get", "post", "patch", "delete"]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)