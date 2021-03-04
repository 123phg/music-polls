import pytest

from genres_polls.exceptions import AnswerValidationException
from genres_polls.factories import QuestionFactory
from genres_polls.models import Question
from music_polls.factories import UserFactory


@pytest.fixture()
def f_user():
    return UserFactory.create()


@pytest.fixture()
def f_question(f_user):
    return QuestionFactory(
        image_url='http://www.test_user_q_1.jpg',
        user=f_user,
        options=['default_option']
    )


@pytest.mark.django_db
def test_should_save_answer(
        f_question
):
    """
    Check, that "answer" Question model method works correctly
    and save selected_answer
    """
    question = f_question
    question.answer('default_option')
    question = Question.objects.get(id=question.pk)
    assert question.selected_answer == 'default_option'


@pytest.mark.django_db
def test_should_catch_correct_exception_via_already_answered_q(
        f_question
):
    """
    Tests, that we cant answer questions, which was answered already
    """
    answer = 'default_option'
    question = f_question
    question.selected_answer = answer
    question.save()

    with pytest.raises(
            AnswerValidationException,
            match=f'Question with id={question.pk} already has an answer'
                  f'Can not save answer={answer}'
    ):
        question.answer(answer)


@pytest.mark.django_db
def test_should_catch_correct_exception_via_wrong_option(
        f_question
):
    """
    Tests, that we cant answer questions with answer text not from options
    """
    answer = 'wrong_option'
    question = f_question

    with pytest.raises(
            AnswerValidationException,
            match=f'Answer={answer} is not in option for question with id={question.pk}'
    ):
        question.answer(answer)
