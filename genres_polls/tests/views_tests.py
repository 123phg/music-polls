import pytest
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from genres_polls.factories import QuestionFactory
from genres_polls.models import Question
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user() -> User:
    return UserFactory.create()


@pytest.fixture()
def f_question(
    f_user: User
) -> Question:
    return QuestionFactory(
        image_url='http://www.test_user_q_2.jpg',
        user=f_user
    )


def _get_client(
    user: User
) -> APIClient:
    client = APIClient()
    client.force_authenticate(user)
    return client


@pytest.mark.django_db
def test_should_return_non_answered_questions(
    f_user: User,
    f_question: Question
) -> None:
    """
    It fixate questions list API response format
    """
    test_user = f_user
    test_user_question = f_question

    client = _get_client(test_user)
    url = reverse('genres_polls_questions-list')
    response = client.get(url)

    assert response.data == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': test_user_question.pk,
                'image_url': 'http://www.test_user_q_2.jpg',
                'options': ['default_option'],
            }
        ]
    }


@pytest.mark.django_db
def test_should_return_one_question(
    f_user: User,
    f_question: Question
) -> None:
    """
    It fixate question detail API response format
    """
    test_user = f_user
    test_user_question = f_question

    client = _get_client(test_user)
    url = reverse('genres_polls_questions-detail', [test_user_question.pk])
    response = client.get(url)

    assert response.data == {
        'id': test_user_question.pk,
        'image_url': 'http://www.test_user_q_2.jpg',
        'options': ['default_option']
    }


@pytest.mark.django_db
def test_should_answer_the_question(
    f_question: Question,
    f_user: User
) -> None:
    """
    Tests, that question can be answer with special DRF action
    """
    test_question = f_question
    test_user = f_user

    client = _get_client(test_user)
    url = reverse('genres_polls_questions-answer', [test_question.pk])

    response = client.patch(
        url,
        data={
            'selected_answer': test_question.options[0]
        }
    )

    assert response.data == {
        'id': test_question.pk,
        'image_url': 'http://www.test_user_q_2.jpg',
        'options': ['default_option'],
        'selected_answer': 'default_option',
        'correct_answer': 'default_option'
    }


@pytest.mark.django_db
def test_should_raise_exception_if_selected_answer_not_provided(
    f_question: Question,
    f_user: User
) -> None:
    """
    If we try to use "answer" action and we provided "selected_answer"
    not from question.options. We should fetch 400 error with correct explanation
    """

    test_question = f_question
    test_user = f_user

    client = _get_client(test_user)
    url = reverse('genres_polls_questions-answer', [test_question.pk])

    response = client.patch(
        url,
        data={
            'selected_answer': 'not valid answer'
        }
    )

    assert response.status_code == 400
    assert response.content.decode("utf-8") == f'["Answer=not valid answer is not' \
                                               f' in option for question with id={test_question.pk}"]'
