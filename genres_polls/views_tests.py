import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from music_polls.factories import UserFactory
from genres_polls.factories import QuestionFactory


@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_user_not_answered_questions_count,'
    'test_user_answered_questions_count,'
    'other_user_not_answered_questions_count,'
    'other_user_answered_questions_count,'
    'expected_api_result',
    [
        (
            0, 3, 5, 4, 0
        )
])
def test_should_return_non_answered_questions(
    test_user_not_answered_questions_count,
    test_user_answered_questions_count,
    other_user_not_answered_questions_count,
    other_user_answered_questions_count,
    expected_api_result
):
    """
    questions list view should return only our user's questions
    this questions should not have answer
    """
    test_user = UserFactory(username='test_user')
    other_user = UserFactory(username='other_user')
    test_user_not_answered_questions = QuestionFactory.create_batch(
        size=test_user_not_answered_questions_count,
        selected_answer=None,
        user=test_user
    )
    test_user_answered_questions = QuestionFactory.create_batch(
        size=test_user_answered_questions_count,
        selected_answer='default_option',
        user=test_user
    )
    other_user_not_answered_questions = QuestionFactory.create_batch(
        size=other_user_not_answered_questions_count,
        selected_answer=None,
        user=other_user
    )
    other_user_answered_questions = QuestionFactory.create_batch(
        size=other_user_answered_questions_count,
        selected_answer='default_option',
        user=other_user
    )

    client = APIClient()
    client.force_authenticate(test_user)
    url = reverse('genres_polls_questions-list')
    response = client.get(url)

    assert len(response.data['results']) == expected_api_result
