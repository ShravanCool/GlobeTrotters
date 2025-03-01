from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from game.tests.factories import DestinationFactory


class SignupViewTest(TestCase):
    def setUp(self):
        self.url = reverse("signup")
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        }
        self.invalid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "securepassword123",
            "password2": "wrongpassword",
        }

        # Create some destinations
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()

    def test_signup_valid(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertRedirects(response, reverse("game_view"))

        self.assertTrue(
            self.client.login(username="testuser", password="securepassword123")
        )

        # Check if the user and profile were created
        user = User.objects.get(username="testuser")
        profile = user.userprofile
        self.assertEqual(profile.score, 0)
        self.assertEqual(profile.games_played, 0)

        # Check success message
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Account created successfully!", messages)

    def test_signup_invalid(self):
        response = self.client.post(self.url, self.invalid_data)

        form = response.context["form"]
        self.assertIn(
            "password2", form.errors
        )  # Check that the field 'password2' has errors
        self.assertEqual(
            form.errors["password2"], ["The two password fields didn’t match."]
        )  # Check the specific error message
