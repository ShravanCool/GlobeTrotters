import json
import logging

from django.core.management.base import BaseCommand

from game.models import Destination

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load destinations from dataset.json into the database"

    def handle(self, *args, **kwargs):
        try:
            with open("dataset.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                destination, created = Destination.objects.update_or_create(
                    city=item["city"],
                    country=item["country"],
                    defaults={
                        "clues": item["clues"],
                        "fun_facts": item["fun_fact"],
                        "trivia": item["trivia"],
                    },
                )
                if created:
                    logger.info(f"Created new destination: {destination}")
                else:
                    logger.info(f"Updated existing destination: {destination}")

            logger.info("Successfully loaded destinations!")

        except Exception as e:
            logger.error(f"Error loading destinations: {e}")
