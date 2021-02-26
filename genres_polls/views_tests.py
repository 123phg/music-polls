import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from genres_polls.factories import QuestionFactory
from genres_polls.models import Question
from music_polls.factories import UserFactory


@pytest.fixture()
def f_users():
    return UserFactory.create_batch(2)


@pytest.mark.parametrize(
    'test_user_questions,'
    'expected_api_result',
    [
        # test_user has two questions with out answers, so api should return two questions
        (
            [
                {
                    'question_image_url': 'http://www.test_user_q_1.jpg',
                    'selected_answer': None
                },
                {
                    'question_image_url': 'http://www.test_user_q_2.jpg',
                    'selected_answer': None
                }
            ],
            {'http://www.test_user_q_1.jpg', 'http://www.test_user_q_2.jpg'}
        ),

        # test_user has one questions w/o answer, so api should return one question
        (
                [
                    {
                        'question_image_url': 'http://www.test_user_q_1.jpg',
                        'selected_answer': 'default_option'
                    },
                    {
                        'question_image_url': 'http://www.test_user_q_2.jpg',
                        'selected_answer': None
                    }
                ],
                {'http://www.test_user_q_2.jpg'}
        ),

        # test_user has not any non answered questions, => api should return empty answer
        (
                [
                    {
                        'question_image_url': 'http://www.test_user_q_1.jpg',
                        'selected_answer': 'default_option'
                    },
                    {
                        'question_image_url': 'http://www.test_user_q_2.jpg',
                        'selected_answer': 'default_option'
                    }
                ],
                set()
        )
    ]
)
@pytest.mark.django_db
def test_should_return_non_answered_questions(
    test_user_questions,
    expected_api_result,
    f_users
):
    """
    It checks, that questions API return questions with out answers

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

    client = APIClient()
    client.force_authenticate(test_user)
    url = reverse('genres_polls_questions-list')
    response = client.get(url)

    response_image_usrls = set(
        result['question_image_url'] for result in response.data['results']
    )

    assert response_image_usrls == expected_api_result


@pytest.mark.parametrize(
    'test_user_questions,'
    'other_user_questions,'
    'expected_api_result',
    [
        (6, 0, 6),
        (0, 6, 0),
        (3, 1, 3),
        (0, 0, 0)
    ]
)
@pytest.mark.django_db
def test_should_check_that_api_return_users_questions(
    test_user_questions,
    other_user_questions,
    expected_api_result,
    f_users
):
    """
    This test check, that questions list API doesn't return other users questions

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

    client = APIClient()
    client.force_authenticate(test_user)
    url = reverse('genres_polls_questions-list')
    response = client.get(url)

    assert len(response.data['results']) == expected_api_result
