import logging
from typing import Dict

from django.db.models.query import QuerySet
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from genres_polls import serializers
from genres_polls.exceptions import AnswerValidationException
from genres_polls.models import Question

logger = logging.getLogger(__name__)


class GenresPollsQuestionViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):

    def get_queryset(self) -> QuerySet:
        return Question.objects.actual_for_user(self.request.user)

    def get_serializers_map(self) -> Dict:
        return {
            self.answer.__name__: serializers.QuestionAnswerSerializer,
            self.list.__name__: serializers.QuestionsSerializer,
            self.retrieve.__name__: serializers.QuestionsSerializer,
        }

    def get_serializer_class(self) -> ModelSerializer:
        try:
            serializer = self.get_serializers_map()[self.action]
        except KeyError as e:
            raise NotImplementedError(f'Unknown action {self.action}')
        return serializer

    @action(detail=True, methods=['patch'])
    def answer(self, request, pk=None) -> Response:
        """
        This action try to set select_answer to question.
        Use in to answer the question.
        """
        question = self.get_object()
        request_serializer = serializers.QuestionAnswerSerializer(data=request.data)
        response_serializer = serializers.QuestionAnswerResponseSerializer(instance=question)

        if not request_serializer.is_valid(raise_exception=True):
            logger.error(
                f'Request data for answer is not valid: {request_serializer.errors}'
            )
            return Response(
                request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        answer = request_serializer.validated_data['selected_answer']
        try:
            question.answer(answer)
        except AnswerValidationException as e:
            logger.error(
                f'Can not answer the question with id={question.pk} with error: {e}'
            )
            raise ValidationError(detail=str(e))
        else:
            return Response(response_serializer.data)
