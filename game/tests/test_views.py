from django.test import TestCase
from django.urls import reverse

from game.constants import CORRECT_ANS_POINTS, INCORRECT_ANS_POINTS
from game.models import Challenge
from game.tests.factories import DestinationFactory
from users.tests.factories import UserFactory, UserProfileFactory


class GameViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password="password123")
        for _ in range(5):
            DestinationFactory()

    def test_game_view_with_valid_user(self):
        response = self.client.get(reverse("game_view"))

        self.assertEqual(response.status_code, 200)

        correct_city = self.client.session.get("correct_city")
        self.assertIsNotNone(correct_city)

        self.assertIn("clues", response.context)
        self.assertIn("choices", response.context)

    def test_game_view_without_login(self):
        self.client.logout()  # Ensure the user is logged out
        response = self.client.get(reverse("game_view"))

        self.assertRedirects(response, f"/accounts/login/?next={reverse('game_view')}")


class SubmitAnswerViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory.create(password="password123")
        self.client.login(username=self.user.username, password="password123")

        self.destination = DestinationFactory(
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

        # Create a user profile
        self.profile = UserProfileFactory(user=self.user)

    def test_submit_correct_answer(self):
        # Set session
        session = self.client.session
        session["correct_city"] = self.destination.city
        session.modified = True
        session.save()

        response = self.client.post(
            reverse("submit_answer"), {"answer": self.destination.city}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["correct"])  # The answer should be correct
        self.assertIn("feedback", data)
        self.assertIn("score", data)
        self.assertIn("games_played", data)

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.score, CORRECT_ANS_POINTS)
        self.assertEqual(self.profile.games_played, 1)
        self.assertEqual(self.client.session["score"], self.profile.score)
        self.assertEqual(self.client.session["games_played"], self.profile.games_played)

    def test_submit_incorrect_answer(self):
        # Set session
        session = self.client.session
        session["correct_city"] = self.destination.city
        session.modified = True
        session.save()

        DestinationFactory(city="Berlin", country="Germany")
        incorrect_answer = "Berlin"  # Incorrect answer
        response = self.client.post(
            reverse("submit_answer"), {"answer": incorrect_answer}
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["correct"])
        self.assertIn("feedback", data)
        self.assertIn("score", data)
        self.assertIn("games_played", data)

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.score, INCORRECT_ANS_POINTS)
        self.assertEqual(self.profile.games_played, 1)
        self.assertEqual(self.client.session["score"], self.profile.score)
        self.assertEqual(self.client.session["games_played"], self.profile.games_played)

    def test_submit_answer_without_login(self):
        self.client.logout()

        response = self.client.post(
            reverse("submit_answer"), {"answer": self.destination.city}
        )

        self.assertRedirects(
            response, f"/accounts/login/?next={reverse('submit_answer')}"
        )


class PlayAgainViewTest(TestCase):
    def test_play_again_redirect(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password=self.user.password)

        response = self.client.get(reverse("play_again"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('play_again')}")


class GenerateChallengeLinkViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(username="testuser", password="password123")
        self.client.force_login(self.user)

    def test_generate_challenge_link(self):
        response = self.client.get(reverse("generate_challenge_link"))

        self.assertEqual(response.status_code, 200)

        challenge = Challenge.objects.first()
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge.inviter, self.user)

        self.assertContains(response, challenge.invite_token)

        challenge_link = response.context["challenge_link"]
        self.assertTrue(challenge_link.startswith("http://"))
        self.assertIn(challenge.invite_token, challenge_link)


class ChallengeViewTest(TestCase):
    def setUp(self):
        self.inviter = UserFactory(username="inviter", password="password123")
        self.client.login(username="inviter", password="password123")

        self.challenge = Challenge.objects.create(
            inviter=self.inviter, invite_token="testtoken"
        )

        self.profile = UserProfileFactory(user=self.inviter, score=100)

    def test_challenge_view(self):
        response = self.client.get(
            reverse("challenge_view", kwargs={"invite_token": "testtoken"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "challenge_page.html")

        self.assertEqual(response.context["challenger_username"], self.inviter.username)
        self.assertEqual(response.context["challenger_score"], self.profile.score)
