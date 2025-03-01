from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from game.tests.factories import DestinationFactory
from users.tests.factories import UserFactory, UserProfileFactory


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

        user = User.objects.get(username="testuser")
        profile = user.userprofile

        self.assertEqual(profile.score, 0)
        self.assertEqual(profile.games_played, 0)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Account created successfully!", messages)

    def test_signup_invalid(self):
        response = self.client.post(self.url, self.invalid_data)

        form = response.context["form"]
        self.assertIn("password2", form.errors)
        self.assertEqual(
            form.errors["password2"], ["The two password fields didn’t match."]
        )


class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse("login")
        self.user = UserFactory()
        self.user_profile = UserProfileFactory(user=self.user)
        self.user.set_password("securepassword123")
        self.user.save()
        self.valid_data = {
            "username": self.user.username,
            "password": "securepassword123",
        }
        self.invalid_data = {"username": "testuser12345", "password": "wrongpassword"}

        # Create some destinations
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()
        DestinationFactory()

    def test_login_valid(self):
        response = self.client.post(self.url, self.valid_data)

        self.assertRedirects(response, reverse("game_view"))

        self.assertEqual(self.client.session.get("score"), 0)
        self.assertEqual(self.client.session.get("games_played"), 0)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Logged in successfully!", messages)

    def test_login_invalid(self):
        response = self.client.post(self.url, self.invalid_data)

        form = response.context["form"]

        self.assertIn("__all__", form.errors)  # Check that there are non-field errors

        self.assertEqual(
            form.errors["__all__"],
            [
                "Please enter a correct username and password. Note that both fields may be case-sensitive."
            ],
        )


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory(email="testuser@example.com", username="testuser")
        self.user.set_password("securepassword123")
        self.user.save()
        self.client.login(username="testuser", password="securepassword123")

    def test_logout(self):
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.get(reverse("logout"))

        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("You have been logged out.", messages)
