import factory
from django.contrib.auth.models import User


# todo: move UserFactory to single application
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'username_{n}@gmail.com')
    first_name = factory.Sequence(lambda n: f'fist_name_{n}@gmail.com')
    last_name = factory.Sequence(lambda n: f'last_name_{n}@gmail.com')
    email = factory.Sequence(lambda n: f'fake_email_{n}@gmail.com')
    password = 'example password'
