# Generated by Django 5.1.6 on 2025-03-01 07:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Destination",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("clues", models.JSONField(default=list)),
                ("fun_facts", models.JSONField(default=list)),
                ("trivia", models.JSONField(default=list)),
            ],
        ),
    ]
