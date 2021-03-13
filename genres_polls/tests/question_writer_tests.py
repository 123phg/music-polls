import pytest

from genres_polls.factories import QuestionFactory
from genres_polls.models import Question as QuestionModel
from genres_polls.question_writer import BaseUserQuestionsWriter, UserQuestionsWriterError, UserQuestionDBWriter
from genres_polls.questions import UserQuestionsRelation, Question as QuestionDTO
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user():
    return UserFactory()


@pytest.fixture()
def f_user_question(f_user):
    return QuestionFactory(
        f_user=f_user
    )


@pytest.fixture()
def f_new_questions(f_user):
    owner = f_user
    questions = [
        QuestionDTO(
            owner=owner,
            album='Congoman',
            artist='The Congos',
            image_url='http://www.image.com/1.jpg',
            options=['Reggie', 'Hip-hop'],
            answer='Reggie'
        ),
        QuestionDTO(
            owner=owner,
            album='King Tubby',
            artist='King Tubby',
            image_url='http://www.image.com/2.jpg',
            options=['Ambient', 'Witchouse', 'Dub'],
            answer='Dub'
        ),
    ]
    return UserQuestionsRelation(
        user=owner,
        questions=questions
    )


@pytest.fixture()
def f_duplicate_questions(f_new_questions):
    duplicate_questions = [
        f_new_questions.questions[0],
        f_new_questions.questions[0]
    ]

    return UserQuestionsRelation(
        user=f_new_questions.user,
        questions=duplicate_questions
    )


def test_checks_correct_writer_argument():
    """
    We should raise exception if BaseUserQuestionsWriter
    was initiate with incorrect argument
    """

    incorrect_argument = {'wrong_arg': True}
    with pytest.raises(
            UserQuestionsWriterError,
            match='Can not initialize UserQuestionsWriter, because '
                  'question_to_user_relation should be UserQuestionsRelation instance.'
    ):
        question_writer = BaseUserQuestionsWriter(incorrect_argument)


@pytest.mark.django_db
def test_should_check_that_questions_unique(
    f_duplicate_questions: UserQuestionsRelation,
):
    """
    Writer should raise exception if we try to write not unique questions
    """
    with pytest.raises(
            UserQuestionsWriterError,
            match='Can not initialize UserQuestionsWriter, because '
                  'question are not unique'
    ):
        question_writer = BaseUserQuestionsWriter(f_duplicate_questions)


@pytest.mark.parametrize(
    'existing_question,'
    'new_questions,'
    'expected_created_questions,'
    'expected_user_questions',
    [
        # there are no any questions in DB, we try to write one question for user
        (
            (),
            [
                {
                    'album':'Congoman',
                    'artist':'The Congos',
                    'image_url':'http://www.image.com/1.jpg',
                    'options':['Reggie', 'Hip-hop'],
                    'answer':'Reggie'
                },
            ],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ]
        ),

        # user already have some questions in DB, but there are no any intersections
        # between existed questions and new questions
        (
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ],
            [
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                }
            ],
            [
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                }
            ],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                },
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                }
            ]
        ),

        # we want to write questions, that already in DB
        (
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ],
            [],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                }
            ]
        ),

        # we want to write some questions, that already in DB, but some of them not exist
        (
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                },
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                }
            ],
            [
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                },
                {
                    'album': 'Game of Thrones',
                    'artist': 'Ramin Djawadi',
                    'image_url': 'http://www.image.com/3.jpg',
                    'options': ['Orchestra', 'Opera'],
                    'answer': 'Orchestra'
                }
            ],
            [
                {
                    'album': 'Game of Thrones',
                    'artist': 'Ramin Djawadi',
                    'image_url': 'http://www.image.com/3.jpg',
                    'options': ['Orchestra', 'Opera'],
                    'answer': 'Orchestra'
                }
            ],
            [
                {
                    'album': 'Congoman',
                    'artist': 'The Congos',
                    'image_url': 'http://www.image.com/1.jpg',
                    'options': ['Reggie', 'Hip-hop'],
                    'answer': 'Reggie'
                },
                {
                    'album': 'Game of Thrones',
                    'artist': 'Ramin Djawadi',
                    'image_url': 'http://www.image.com/3.jpg',
                    'options': ['Orchestra', 'Opera'],
                    'answer': 'Orchestra'
                },
                {
                    'album': 'King Tubby',
                    'artist': 'King Tubby',
                    'image_url': 'http://www.image.com/2.jpg',
                    'options': ['Ambient', 'Witchouse', 'Dub'],
                    'answer': 'Dub'
                }
            ]
        )
    ]
)
@pytest.mark.django_db
def test_should_check_data_was_written_to_db(
    existing_question,
    new_questions,
    expected_created_questions,
    expected_user_questions,
    f_user
):
    """
    Tests that questions data was correctly loaded to DB.

    Checks:
     - data in db is equal to data in fixture
     - if we have duplicates questions in db and in array, that we wont to write,
       we should deduplicate them

    Cases:
     - user have not questions, we write some new questions,
     - user have some questions, new questions have not any intersections,
     - user have some questions, we want to write questions, that already exists,
     - user have some questions, we have some of them in intersection
    """
    # todo: refactor QuestionDTO: remove user relation and refactor this test after
    questions_owner = f_user

    existing_questions = [
        QuestionModel(
            user=questions_owner,
            album=question['album'],
            artist=question['artist'],
            image_url=question['image_url'],
            options=question['options'],
            correct_answer=question['answer'],
        ) for question in existing_question
    ]
    QuestionModel.objects.bulk_create(existing_questions)

    questions_user_relation = UserQuestionsRelation(
        user=questions_owner,
        questions=[
            QuestionDTO(
                owner=questions_owner,
                answer=question['answer'],
                album=question['album'],
                artist=question['artist'],
                image_url=question['image_url'],
                options=question['options']
            ) for question in new_questions
        ]
    )

    writer = UserQuestionDBWriter(questions_user_relation)
    created_questions = writer.write()

    # check created questions
    for index, question in enumerate(created_questions):
        assert question.artist == expected_created_questions[index]['artist']
        assert question.album == expected_created_questions[index]['album']
        assert question.image_url == expected_created_questions[index]['image_url']
        assert question.options == expected_created_questions[index]['options']
        assert question.correct_answer == expected_created_questions[index]['answer']

    # check all existing questions for target user
    user_questions = QuestionModel.objects.filter(user=questions_owner).order_by('-artist')
    assert len(user_questions) == len(expected_user_questions)
    for index, question in enumerate(user_questions):
        assert question.artist == expected_user_questions[index]['artist']
        assert question.album == expected_user_questions[index]['album']
        assert question.image_url == expected_user_questions[index]['image_url']
        assert question.options == expected_user_questions[index]['options']
        assert question.correct_answer == expected_user_questions[index]['answer']
