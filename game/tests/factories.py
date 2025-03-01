import factory
from factory import Faker, fuzzy
from factory.django import DjangoModelFactory

from game.models import Challenge, Destination
from users.tests.factories import UserFactory


class DestinationFactory(DjangoModelFactory):
    class Meta:
        model = Destination

    city = Faker("city")
    country = Faker("country")
    clues = [fuzzy.FuzzyText(length=30).fuzz(), fuzzy.FuzzyText(length=30).fuzz()]
    fun_facts = [fuzzy.FuzzyText(length=30).fuzz(), fuzzy.FuzzyText(length=30).fuzz()]
    trivia = [fuzzy.FuzzyText(length=30).fuzz(), fuzzy.FuzzyText(length=30).fuzz()]


class ChallengeFactory(DjangoModelFactory):
    class Meta:
        model = Challenge

    inviter = factory.SubFactory(UserFactory)
    invitee = factory.SubFactory(UserFactory)
    invite_token = Faker("uuid4")  # Generates a unique invite token
    created_at = factory.Faker("date_time_this_year", tzinfo=None)
