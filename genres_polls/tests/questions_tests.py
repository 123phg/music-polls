import pytest

from genres_polls.questions import QuestionValidationError, Question
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user():
    return UserFactory.create()


@pytest.mark.parametrize(
    'image_url,'
    'options,'
    'answer,'
    'error_message',
    [
        (
            'http://www.image-server.com/example_image.jpg',
            ['ambient', 'lo-fi'],
            'dubstep',
            'Incorrect Question: there are no answer "dubstep" in options: "ambient,lo-fi"'
        ),
        (
            'test_incorrect_url',
            ['ambient', 'lo-fi'],
            'ambient',
            'Question image_url field is incorrect: "test_incorrect_url"'
        )
    ]
)
@pytest.mark.django_db
def test_should_check_question_validation(
    image_url,
    options,
    answer,
    error_message,
    f_user
):
    """
    Tests, that we can not create incorrect Question entity:
    - answer should be in options
    - image url should be valid URL
    """
    with pytest.raises(
            QuestionValidationError,
            match=error_message
    ):
        question = Question(
            owner=f_user,
            album='example_album',
            artist='example_artist',
            image_url=image_url,
            options=options,
            answer=answer
        )
