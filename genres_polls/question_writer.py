import logging
from abc import ABCMeta, abstractmethod
from typing import List

from genres_polls.models import Question as QuestionModel
from genres_polls.questions import UserQuestionsRelation, Question as QuestionDTO

logger = logging.getLogger(__name__)


class UserQuestionsWriterError(Exception):
    pass


class QuestionAbstractWriter(metaclass=ABCMeta):
    """
    Abstract interface class for question writers
    """

    @abstractmethod
    def write(self):
        ...


class BaseUserQuestionsWriter(QuestionAbstractWriter):
    """
    This writer can store NEW questions for the user.
    In case of successful registration, questions will be available
    in questions API.
    It can work with UserQuestionsRelation as a params only,
    because we should be sure, that all questions,
    that we wont to write are owned by one user.
    """

    def __init__(
        self,
        question_to_user_relation: UserQuestionsRelation
    ) -> None:
        self.question_to_user_relation = question_to_user_relation

    @property
    def question_to_user_relation(self) -> UserQuestionsRelation:
        return self._question_to_user_relation

    @question_to_user_relation.setter
    def question_to_user_relation(
        self,
        relation: UserQuestionsRelation
    ) -> None:
        if not isinstance(relation, UserQuestionsRelation):
            raise UserQuestionsWriterError(
                'Can not initialize UserQuestionsWriter, because '
                'question_to_user_relation should be UserQuestionsRelation instance.'
            )

        self._validate_questions(relation.questions)
        self._question_to_user_relation = relation

    def _validate_questions(
        self,
        questions: List[QuestionDTO]
    ) -> None:
        """
        Each artist's album has individual album's cover.
        So, all questions, that we wont to write should be unique
        by 'album' and 'answer' fields.
        """
        artists_albums = [
            (question.artist, question.album) for question in questions
        ]

        if len(set(artists_albums)) != len(artists_albums):
            raise UserQuestionsWriterError(
                'Can not initialize UserQuestionsWriter, because '
                'question are not unique'
            )

    def write(self) -> None:
        raise NotImplementedError()


class UserQuestionDBWriter(BaseUserQuestionsWriter):
    """
    This writer store questions data into django db.
    Before write data, writer check questions and filter questions,
    thar already exist in data base for target user.
    """

    def _prepare_questions(self) -> List[QuestionDTO]:
        """
        Method removes questions, which are already exist in DB
        """
        exist_questions = set(
            QuestionModel.objects.filter(
                user=self.question_to_user_relation.user
            ).values_list('artist', 'album')
        )

        new_questions_map = {
            (question.artist, question.album): question
            for question in self.question_to_user_relation.questions
        }

        questions_to_write_keys = set(new_questions_map) - exist_questions
        questions_to_write = []
        for question_key in questions_to_write_keys:
            questions_to_write.append(
                new_questions_map[question_key]
            )
        skipped_questions_len = len(new_questions_map) - len(questions_to_write)

        logger.info(
            f'{skipped_questions_len} questions was skipped to write.'
        )

        return questions_to_write

    def write(self) -> List[QuestionModel]:
        """
        Write questions for user.
        If there are duplicates in questions, an error will occur.
        We don't wont to write questions, if some of them are exist for user in DB,
        so we filter them.
        """
        questions = self._prepare_questions()

        questions_objects = [
            QuestionModel.objects.from_question_dto(question) for question in questions
        ]

        new_questions = QuestionModel.objects.bulk_create(questions_objects)
        _new_questions_ids = ','.join(
            str(question.id) for question in new_questions
        )
        logger.info(
            f'Questions with ids={_new_questions_ids} '
            f'for user={self.question_to_user_relation.user}'
            f'was written to database.'
        )
        return new_questions
