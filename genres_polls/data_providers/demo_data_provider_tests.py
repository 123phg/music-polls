import pytest
from django.contrib.auth.models import User
from music_polls.factories import UserFactory
from genres_polls.data_providers import DemoDataProvider
from genres_polls.questions import Question as QuestionDTO


@pytest.fixture()
def f_user() -> User:
    return UserFactory.create(
        username='first_test_user'
    )


@pytest.mark.parametrize(
    'exist_questions',
    [
        (),
        (
            QuestionDTO(
                album="SM007V",
                artist="Dasha Rush",
                image_url="https://i1.sndcdn.com/artworks-000128864984-c0etzi-t500x500.jpg",
                options=["2016", "2006"],
                answer="2016"
            )
        )
    ]
)
@pytest.mark.django_db
def test_should_return_deduplicate_questions(
    exist_questions,
    f_user: User
) -> None:
    """
    We should be sure, that demo data provider will not return questions,
    which already exist for target user
    """

