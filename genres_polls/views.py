from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from genres_polls import serializers
from genres_polls.models import Question


class GenresPollsQuestionViewSet(mixins.ListModelMixin, GenericViewSet):
    def get_queryset(self):
        return Question.objects.filter(
            user=self.request.user,
            selected_answer=None
        )

    def get_serializer_class(self):
        return serializers.GenresPollQuestionsSerializer
