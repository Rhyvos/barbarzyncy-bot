from django.core.management.base import BaseCommand

from django.conf import settings as project_settings
from dotenv import dotenv_values
from .bot.utils.update_bot import check_for_updates

settings = dotenv_values(project_settings.ENV_PATH)


class Command(BaseCommand):
    help = "Updates bot"

    def handle(self, *args, **options):
        return check_for_updates()
