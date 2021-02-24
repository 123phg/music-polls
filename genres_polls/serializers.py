from rest_framework import serializers

from genres_polls.models import Question


class GenresPollQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question_image_url',
            'options',
        )
