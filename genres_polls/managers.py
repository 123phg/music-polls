from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet

from genres_polls.questions import Question as QuestionDTO


class QuestionManager(models.Manager):
    def actual_for_user(
        self,
        user: User
    ) -> QuerySet:
        """
        Fetch not answered questions for user
        """
        return self.filter(
            user=user,
            selected_answer=None
        )

    def from_question_dto(
        self,
        question_dto: QuestionDTO
    ) -> models.Model:
        """
        Convert Question data transfer object to Question model object
        """
        return self.model(
            user=question_dto.owner,
            album=question_dto.album,
            artist=question_dto.artist,
            image_url=question_dto.image_url,
            options=question_dto.options,
            correct_answer=question_dto.answer
        )
