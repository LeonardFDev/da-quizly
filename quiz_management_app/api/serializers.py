"""Serializers for Quiz and Question API operations."""

from rest_framework import serializers
from urllib.parse import urlparse

from quiz_management_app.models import Quiz, Question
from services.transcriber import generate_quiz


class QuestionSerializer(serializers.ModelSerializer):
    """Nested serializer for the Question model in QuizSerializer (except POST requests)."""
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer"]
        read_only_fields = ["id", "question_title", "question_options", "answer"]


class QuestionPostSerializer(serializers.ModelSerializer):
    """Nested serializer for the Question model in QuizSerializer (only POST requests)."""
    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]
        read_only_fields = ["id", "question_title", "question_options", "answer", "created_at", "updated_at"]


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for the Quiz model."""

    url = serializers.URLField(write_only=True)
    questions = QuestionSerializer(many=True, source="quiz_question", read_only = True)

    class Meta:
        model = Quiz
        fields = ["id", "title", "description", "created_at", "updated_at", "url", "video_url", "questions"]
        read_only_fields = ["id", "title", "description", "created_at", "updated_at", "video_url", "questions"]

    def __init__(self, *args, **kwargs):
        """"at "PATCH" sets the title and description to "False" for read only and "True" for the URL.
            at "POST" the questions field gets another serializer."""
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request and request.method == "PATCH":
            self.fields["title"].read_only = False
            self.fields["description"].read_only = False
            self.fields["url"].read_only = True
            
        if request and request.method == "POST":
            self.fields["questions"] = QuestionPostSerializer(many=True, source="quiz_question", read_only=True)

    
    def create(self, validated_data):
        """Create quiz and questions."""
        self.customized_validated_video_url(validated_data)

        ai_output = generate_quiz(validated_data["video_url"])
        self.validation_errors(ai_output)

        validated_data["title"] = ai_output.get("title")
        validated_data["description"] = ai_output.get("description")
        quiz = Quiz.objects.create(**validated_data)

        questions_data = ai_output.get("questions")
        for question_data in questions_data:
            Question.objects.create(quiz=quiz, **question_data)
        return quiz

    def customized_validated_video_url(self, validated_data):
        """In the case of a youtu.be link, it is changed to youtube.com link."""
        validated_data["video_url"] = validated_data.pop("url")
        
        url_info = urlparse(validated_data["video_url"])
        if url_info.hostname == "youtu.be":
            validated_data["video_url"]= f"https://www.youtube.com/watch?v={url_info.path.strip("/")}"

    def validation_errors(self, ai_output):
        """checks if the AI output has an error and outputs it if necessary."""
        ai_output_error = ai_output.get("ai_output_error")
        
        if ai_output.get("is_audio_download_error") == True:
            raise serializers.ValidationError({"error_message": "No audio could be extracted under this url."})
        elif ai_output_error and ai_output_error.code == 503:
            raise serializers.ValidationError({"error_message": "The servers are overloaded. Please try again later."})
        elif ai_output.get("is_ai_error") == True:
            raise serializers.ValidationError({"error_message": "An unknown error has occurred. Please try again later."})
        elif ai_output.get("is_json_error") == True:
            raise serializers.ValidationError({"error_message": "There was an error in the output of the AI, please try again or try a different url"})

        self.incorrect_json(ai_output)

    def incorrect_json(self, ai_output):
        """checks if the output for Quiz and Questions is a valid json"""
        self.incorrect_json_question(ai_output)
        self.incorrect_json_quiz(ai_output)

    def incorrect_json_question(self, ai_output):
        """Checks if the output for questions is a valid JSON, if not, it throws a ValidationError."""
        questions_data = ai_output.get("questions")
        
        expected_keys_question = {"question_title", "question_options", "answer"}

        for question_data in questions_data or []:
            if set(question_data.keys()) != expected_keys_question:
                raise serializers.ValidationError({"error": "The AI output an incorrect JSON structure. Please try again"})

    def incorrect_json_quiz(self, ai_output):
        """Checks if the output for quiz is a valid JSON, if not, it throws a ValidationError."""
        expected_keys_quiz = {"title", "description", "questions"}

        if set(ai_output.keys()) != expected_keys_quiz:
            raise serializers.ValidationError({"error": "The AI output an incorrect JSON structure. Please try again"})