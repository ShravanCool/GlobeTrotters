from django.test import TestCase
from users.tests.factories import UserFactory, UserProfileFactory


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()
        cls.user_profile1 = UserProfileFactory(user=cls.user1)

    def setUp(self):
        self.user_profile2 = UserProfileFactory()

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile2.score, 0)
        self.assertEqual(self.user_profile2.games_played, 0)
        self.assertEqual(
            str(self.user_profile2),
            f"{self.user_profile2.user.username} - Score: {self.user_profile2.score}",
        )

    def test_increment_score(self):
        self.user_profile2.increment_score(points=5)
        self.assertEqual(self.user_profile2.score, 5)
        self.assertEqual(self.user_profile2.games_played, 1)
