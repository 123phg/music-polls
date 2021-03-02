import logging

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

from genres_polls.exceptions import AnswerValidationException
from genres_polls.managers import QuestionManager

logger = logging.getLogger(__name__)


class Question(models.Model):
    # todo: add linkkey field and request questions via linkkey
    objects = QuestionManager()

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    # todo: rename "question_image_url" field to "image_url"
    question_image_url = models.URLField(
        max_length=512
    )
    options = ArrayField(
        base_field=models.CharField(
            max_length=128,
            null=False,
            blank=False
        )
    )
    correct_answer = models.CharField(
        max_length=128,
    )
    selected_answer = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def answer(self, answer):
        """
        Use this method to set answer the question
        """
        logger.info(
            f'Try to save answer "{answer}" to question with id={self.pk}'
        )
        self.validate_answer(answer)
        self.selected_answer = answer
        self.save()

    def validate_answer(self, answer):
        """
        Check, that answer in options
        Check, that questions have not any answer
        """
        if self.selected_answer is not None:
            raise AnswerValidationException(
                f'Question with id={self.pk} already has an answer'
                f'Can not save answer={answer}'
            )

        if answer not in self.options:
            raise AnswerValidationException(
                f'Answer={answer} is not in option for question with id={self.pk}'
            )
