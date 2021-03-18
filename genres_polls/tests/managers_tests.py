from typing import Iterable, List, Dict, Set

import pytest
from django.contrib.auth.models import User

from genres_polls.factories import QuestionFactory
from genres_polls.models import Question
from genres_polls.questions import Question as QuestionDTO
from music_polls.factories import UserFactory


@pytest.fixture()
def f_users() -> Iterable[User]:
    return UserFactory.create_batch(2)


@pytest.fixture()
def f_question_dto(f_users) -> QuestionDTO:
    owner, _ = f_users
    return QuestionDTO(
        owner=owner,
        album='Bad / Badder',
        artist='Calibre',
        image_url='http://www.calibre.com/images/bad.jpg',
        options=['ambient', 'dub'],
        answer='ambient'
    )


@pytest.mark.parametrize(
    'test_user_questions,'
    'expected_result',
    [
        # test_user has two questions with out answers, so manager should return two questions
        (
            [
                {
                    'image_url': 'http://www.test_user_q_1.jpg',
                    'selected_answer': None
                },
                {
                    'image_url': 'http://www.test_user_q_2.jpg',
                    'selected_answer': None
                }
            ],
            {'http://www.test_user_q_1.jpg', 'http://www.test_user_q_2.jpg'}
        ),

        # test_user has one questions w/o answer, so manager should return one question
        (
                [
                    {
                        'image_url': 'http://www.test_user_q_1.jpg',
                        'selected_answer': 'default_option'
                    },
                    {
                        'image_url': 'http://www.test_user_q_2.jpg',
                        'selected_answer': None
                    }
                ],
                {'http://www.test_user_q_2.jpg'}
        ),

        # test_user has not any non answered questions, => manager should return empty answer
        (
                [
                    {
                        'image_url': 'http://www.test_user_q_1.jpg',
                        'selected_answer': 'default_option'
                    },
                    {
                        'image_url': 'http://www.test_user_q_2.jpg',
                        'selected_answer': 'default_option'
                    }
                ],
                set()
        )
    ]
)
@pytest.mark.django_db
def test_should_return_non_answered_questions(
    test_user_questions: List[Dict],
    expected_result: Set[str],
    f_users: List[User]
) -> None:
    """
    It checks, that questions model manager returns questions with out answers

    Cases:
    - test user has some questions with out answers
    - test user has some questions w/o answers and some questions with answers
    - test user has questions with answers only
    """
    test_user, _ = f_users

    test_user_questions = [
        QuestionFactory.build(
            **question_param,
            user=test_user
        ) for question_param in test_user_questions
    ]
    Question.objects.bulk_create(test_user_questions)

    questions_wo_answers = Question.objects.actual_for_user(test_user)
    result_image_urls = {question.image_url for question in questions_wo_answers}

    assert result_image_urls == expected_result


@pytest.mark.parametrize(
    'test_user_questions,'
    'other_user_questions,'
    'expected_result',
    [
        (6, 0, 6),
        (0, 6, 0),
        (3, 1, 3),
        (0, 0, 0)
    ]
)
@pytest.mark.django_db
def test_should_check_that_api_return_users_questions(
    test_user_questions: int,
    other_user_questions: int,
    expected_result: int,
    f_users: List[User]
) -> None:
    """
    This test check, that questions model manager doesn't return other users questions

    Cases:
    - user has some questions, but other user has not
    - user has not any questions, but other user has
    - both users have questions
    - both users have not questions
    """

    test_user, other_user = f_users

    QuestionFactory.create_batch(
        size=test_user_questions,
        user=test_user
    )
    QuestionFactory.create_batch(
        size=other_user_questions,
        user=other_user
    )

    test_user_questions_len = len(Question.objects.actual_for_user(test_user))
    other_user_questions_len = len(Question.objects.actual_for_user(other_user))
    assert test_user_questions_len == expected_result
    assert len(Question.objects.all()) - test_user_questions_len == other_user_questions_len


@pytest.mark.django_db
def test_create_question_from_dto(
        f_question_dto: QuestionDTO
) -> None:
    """
    Tests, that 'from_dto' method of Question model manager returns
    correct model object entity
    """
    question_model_object = Question.objects.from_question_dto(f_question_dto)
    assert question_model_object.user == f_question_dto.owner
    assert question_model_object.album == f_question_dto.album
    assert question_model_object.artist == f_question_dto.artist
    assert question_model_object.image_url == f_question_dto.image_url
    assert question_model_object.options == f_question_dto.options
    assert question_model_object.correct_answer == f_question_dto.answer
