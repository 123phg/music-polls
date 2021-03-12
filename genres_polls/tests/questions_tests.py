import pytest

from genres_polls.questions import QuestionValidationError, Question, UserQuestionsRelation
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user():
    return UserFactory.create(
        username='first_test_user'
    )


@pytest.fixture()
def f_other_user():
    return UserFactory.create(
        username='second_test_user'
    )


@pytest.fixture()
def f_first_user_question(f_user):
    return Question(
        owner=f_user,
        album='example_album',
        artist='example_artist',
        image_url='http://www.image-server.com/example_image.jpg',
        options=['hip-hop', 'blues'],
        answer='blues'
    )


@pytest.fixture()
def f_second_user_question(f_other_user):
    return Question(
        owner=f_other_user,
        album='example_album',
        artist='example_artist',
        image_url='http://www.image-server.com/example_image2.jpg',
        options=['dark jazz', 'blues'],
        answer='dark jazz'
    )


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


@pytest.mark.django_db
def test_should_check_question_relation_answer(
    f_user,
    f_first_user_question,
    f_second_user_question
):
    """
    Tests, that we can not create user-questions relations
    with questions, owned by other user
    """
    first_user = f_user
    first_user_question = f_first_user_question
    second_user_question = f_second_user_question
    with pytest.raises(
            QuestionValidationError,
            match='Can not create questions to user relation because '
                  'one or more questions is not owned by user first_test_user'
    ):
        user_questions_rel = UserQuestionsRelation(
            user=first_user,
            questions=[first_user_question, second_user_question]
        )
