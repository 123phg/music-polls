from django.contrib.auth.models import User
from django.db import models

from genres_polls.questions import Question


class QuestionManager(models.Manager):
    def actual_for_user(
        self,
        user: User
    ):
        """
        Fetch not answered questions for user
        """
        return self.filter(
            user=user,
            selected_answer=None
        )

    def from_question_dto(
        self,
        question_dto: Question
    ):
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
