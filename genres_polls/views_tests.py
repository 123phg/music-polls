import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from genres_polls.factories import QuestionFactory
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user():
    return UserFactory.create()


@pytest.mark.django_db
def test_should_return_non_answered_questions(f_user):
    """
    It fixate API response format
    """
    test_user = f_user
    test_user_question = QuestionFactory(
        question_image_url='http://www.test_user_q_2.jpg',
        user=test_user
    )

    client = APIClient()
    client.force_authenticate(test_user)
    url = reverse('genres_polls_questions-list')
    response = client.get(url)

    assert response.data == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': test_user_question.pk,
                'question_image_url': 'http://www.test_user_q_2.jpg',
                'options': ['default_option'],
            }
        ]
    }
