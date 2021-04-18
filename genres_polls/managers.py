from django.contrib.auth.models import User
from django.db import models
from django.db.models.query import QuerySet
import logging
from genres_polls.questions import Question as QuestionDTO
from typing import List

logger = logging.getLogger(__name__)

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

    # todo: refactor tests and separate writer's tests and check deduplicate_user_questions
    def deduplicate_user_questions(
        self,
        user: User,
        questions: List[QuestionDTO]
    ) -> List[QuestionDTO]:
        """
        Method removes questions, which are already exist in DB
        """
        exist_questions = set(
            self.model.objects.filter(
                user=user
            ).values_list('artist', 'album')
        )

        new_questions_map = {
            (question.artist, question.album): question
            for question in questions
        }

        result_questions_keys = set(new_questions_map) - exist_questions
        result_questions = []
        for question_key in result_questions_keys:
            result_questions.append(
                new_questions_map[question_key]
            )
        skipped_questions_len = len(new_questions_map) - len(result_questions)

        logger.info(
            f'{skipped_questions_len} questions was skipped to write.'
        )

        return result_questions
