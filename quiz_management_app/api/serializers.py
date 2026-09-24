from rest_framework import serializers

from quiz_management_app.models import Quiz, Question
from services.transcriber import download_and_transcribe


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]
        read_only_fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]


class QuizzeCreateSerializer(serializers.ModelSerializer):
    url = serializers.CharField(write_only=True)
    questions = QuestionSerializer(many=True, source="quiz_question", read_only = True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", "updated_at", "url", "video_url", "questions"]
        read_only_fields = ["id", "title", "description", "created_at", "updated_at", "video_url", "questions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request and request.method == "PATCH":
            self.fields["title"].read_only = False
            self.fields["description"].read_only = False

    def create(self, validated_data):
        validated_data["video_url"] = validated_data.pop("url")
        download_and_transcribe(validated_data["video_url"])

        
        return super().create(validated_data)