import random
from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    clues = models.JSONField(default=list)  # Stores exactly 2 clues as a list
    fun_facts = models.JSONField(default=list)  # Stores exactly 2 fun facts as a list
    trivia = models.JSONField(default=list)  # Stores exactly 2 trivia points as a list

    class Meta:
        unique_together = ("city", "country")

    def __str__(self):
        return f"{self.city}, {self.country}"

    def get_random_fun_fact(self):
        return random.choice(self.fun_facts)

    def get_random_trivia(self):
        return random.choice(self.trivia)

    @classmethod
    def get_random_destination(cls):
        return random.choice(cls.objects.all())

    @classmethod
    def get_answer_choices(cls, instance):
        choices = [instance.city] + [
            d.city
            for d in random.sample(list(Destination.objects.exclude(id=instance.id)), 3)
        ]
        random.shuffle(choices)
        return choices


class Challenge(models.Model):
    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invites"
    )
    invitee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_invites",
    )
    invite_token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
