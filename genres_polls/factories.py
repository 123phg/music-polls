import factory

from genres_polls.models import Question
from music_polls.factories import UserFactory


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    user = factory.SubFactory(UserFactory)
    question_image_url = factory.Sequence(lambda n: f'http://www.images.com/image_{n}.jpg')
    options = ['default_option']
