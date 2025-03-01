import factory
from factory.django import DjangoModelFactory  # Factory for creating User objects
from django.contrib.auth.models import User

from users.models import UserProfile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")


# Factory for creating UserProfile objects
class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory)
    score = 0
    games_played = 0
