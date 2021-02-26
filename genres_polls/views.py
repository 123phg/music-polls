from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from genres_polls import serializers
from genres_polls.models import Question


class GenresPollsQuestionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    def get_queryset(self):
        return Question.objects.actual_for_user(self.request.user)

    def get_serializer_class(self):
        return serializers.GenresPollQuestionsSerializer
