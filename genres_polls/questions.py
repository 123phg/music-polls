import dataclasses
from typing import List

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


class QuestionValidationError(Exception):
    pass


@dataclasses.dataclass(frozen=True)
class Question:
    """
    Use Question as data transfer object between apps.
    """
    owner: User
    album: str
    artist: str
    image_url: str
    options: List[str]
    answer: str

    def __post_init__(self):
        self._validate_fields()

    def _validate_fields(self):
        self._validate_answer()
        self._validate_image_url()

    def _validate_answer(self):
        if self.answer not in self.options:
            _options = ','.join(self.options)
            raise QuestionValidationError(
                f'Incorrect Question: there are no answer "{self.answer}" '
                f'in options: "{_options}"'
            )

    def _validate_image_url(self):
        validate = URLValidator()
        try:
            validate(self.image_url)
        except ValidationError as e:
            raise QuestionValidationError(
                f'Question image_url field is incorrect: "{self.image_url}"'
            )


@dataclasses.dataclass(frozen=True)
class UserQuestionsRelation:
    """
    This class store relation between user and his questions.
    """
    user: User
    questions: List[Question]

    def __post_init__(self):
        self._validate_user_questions_relation()

    def _validate_user_questions_relation(self):
        """
        Each question from self.questions should be owned by self.user
        """
        for question in self.questions:
            if question.owner != self.user:
                raise QuestionValidationError(
                    f'Can not create questions to user relation '
                    f'because one or more questions is not owned by user {self.user}'
                )
