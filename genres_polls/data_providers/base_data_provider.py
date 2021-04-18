from abc import ABCMeta, abstractmethod
from django.contrib.auth.models import User
from typing import List
from genres_polls.questions import Question as QuestionDTO, UserQuestionsRelation
from genres_polls.models import Question as QuestionModel
import json
import os


class DataProvider(metaclass=ABCMeta):
    @abstractmethod
    def get_data(self) -> List[QuestionDTO]:
        ...


class DemoDataProvider(DataProvider):
    DEMO_DATA_FILE = 'demo_data.json'

    def __init__(
        self,
        user: User
    ) -> None:
        self.user = user

    def _get_demo_data_file_path(self) -> str:
        return os.path.join(
            os.path.dirname(__file__),
            self.DEMO_DATA_FILE
        )

    def _get_data_from_file(self) -> List[QuestionDTO]:
        with open(
            self._get_demo_data_file_path(),
            'r'
        ) as json_file:
            demo_questions_data = json.load(json_file)
            questions = []
            for question in demo_questions_data:
                questions.append(
                    QuestionDTO(**question)
                )
            return questions

    def get_data(self) -> List[QuestionDTO]:
        questions = self._get_data_from_file()
        result_questions = QuestionModel.objects.deduplicate_user_questions(
            self.user,
            questions
        )
        return result_questions







