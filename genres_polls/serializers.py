from rest_framework import serializers

from genres_polls.models import Question


# todo: rename "GenresPollQuestionsSerializer" to "QuestionSerializer"
class GenresPollQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question_image_url',
            'options',
        )


class QuestionAnswerSerializer(serializers.ModelSerializer):
    selected_answer = serializers.CharField(required=True)

    class Meta:
        model = Question
        fields = (
            'selected_answer',
        )


class QuestionAnswerResponseSerializer(serializers.ModelSerializer):
    """
    Uses to show result question data after answering.
    """

    class Meta:
        model = Question
        fields = (
            'id',
            'question_image_url',
            'options',
            'selected_answer',
            'correct_answer',
        )
