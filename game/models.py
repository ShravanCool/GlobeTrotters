from django.db import models


class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    clues = models.JSONField(default=list)  # Stores exactly 2 clues as a list
    fun_facts = models.JSONField(default=list)  # Stores exactly 2 fun facts as a list
    trivia = models.JSONField(default=list)  # Stores exactly 2 trivia points as a list

    def __str__(self):
        return f"{self.city}, {self.country}"
