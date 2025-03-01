from django.contrib.auth.models import User
from django.test import TestCase

from users.forms import UserRegistrationForm


class UserRegistrationFormTest(TestCase):
    def test_form_with_valid_data(self):
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "strong_password123",
                "password2": "strong_password123",
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_with_missing_email(self):
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "password1": "strong_password123",
                "password2": "strong_password123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_with_invalid_email(self):
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "email": "not-an-email",
                "password1": "strong_password123",
                "password2": "strong_password123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_form_with_password_mismatch(self):
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "strong_password123",
                "password2": "mismatch_password",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_with_short_password(self):
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "short",
                "password2": "short",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_with_existing_username(self):
        User.objects.create_user(
            username="testuser", email="testuser1@example.com", password="password123"
        )
        form = UserRegistrationForm(
            data={
                "username": "testuser",
                "email": "testuser2@example.com",
                "password1": "strong_password123",
                "password2": "strong_password123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
