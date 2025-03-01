from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    highest_score = models.IntegerField(default=0)

    def increment_score(self, points=3):
        self.score += points
        self.games_played += 1
        if self.score > self.highest_score:
            self.highest_score = self.score
        self.save()

    def __str__(self):
        return f"{self.user.username} - Score: {self.score}"
