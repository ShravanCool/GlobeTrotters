from django.test import TestCase

from game.models import Challenge, Destination
from game.tests.factories import ChallengeFactory, DestinationFactory
from users.tests.factories import UserFactory


class DestinationModelTest(TestCase):
    def test_create_destination(self):
        destination = DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )

        self.assertEqual(destination.city, "Paris")
        self.assertEqual(destination.country, "France")
        self.assertEqual(len(destination.clues), 2)
        self.assertEqual(len(destination.fun_facts), 2)
        self.assertEqual(len(destination.trivia), 2)

    def test_unique_together_constraint(self):
        DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )

        with self.assertRaises(Exception):
            DestinationFactory.create(
                city="Paris",
                country="France",
                clues=["Notre-Dame Cathedral", "Champs-Élysées"],
                fun_facts=[
                    "It's known for its art",
                    "It has over 2 million visitors each year",
                ],
                trivia=[
                    "The first university was founded in Paris",
                    "The French Revolution started here",
                ],
            )

    def test_get_random_fun_fact(self):
        destination = DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )

        random_fun_fact = destination.get_random_fun_fact()
        self.assertIn(random_fun_fact, destination.fun_facts)

    def test_get_random_trivia(self):
        destination = DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )

        random_trivia = destination.get_random_trivia()
        self.assertIn(random_trivia, destination.trivia)

    def test_get_random_destination(self):
        destination1 = DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )
        destination2 = DestinationFactory.create(
            city="London",
            country="UK",
            clues=["Big Ben", "Buckingham Palace"],
            fun_facts=["It's the capital of the UK", "It has over 8 million residents"],
            trivia=[
                "The River Thames runs through it",
                "It was founded in Roman times",
            ],
        )

        random_destination = Destination.get_random_destination()
        self.assertIn(random_destination, [destination1, destination2])

    def test_get_answer_choices(self):
        destination1 = DestinationFactory.create(
            city="Paris",
            country="France",
            clues=["The Eiffel Tower", "Louvre Museum"],
            fun_facts=[
                "It's the most visited city in the world",
                "It has over 2 million residents",
            ],
            trivia=[
                "It was founded in the 3rd century BC",
                "The Seine River runs through it",
            ],
        )
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()

        answer_choices = Destination.get_answer_choices(destination1)
        self.assertIn(destination1.city, answer_choices)
        self.assertEqual(len(answer_choices), 4)


class ChallengeModelTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

    def test_unique_invite_token(self):
        ChallengeFactory.create(
            inviter=self.user1, invitee=self.user2, invite_token="randomtoken123"
        )
        with self.assertRaises(Exception):
            ChallengeFactory.create(
                inviter=self.user1,
                invitee=self.user2,
                invite_token="randomtoken123",  # Duplicate invite_token
            )
