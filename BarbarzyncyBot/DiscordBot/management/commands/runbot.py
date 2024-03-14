from django.core.management.base import BaseCommand

from django.conf import settings as project_settings
from dotenv import dotenv_values
from .bot.BotBarbarzynca import BotBarbarzynca
from .bot.utils.bot_logger import bot_log_handler, bot_log_format

settings = dotenv_values(project_settings.ENV_PATH)


class Command(BaseCommand):
    help = "Runs the bot"
    bot_log_handler = bot_log_handler()

    def handle(self, *args, **options):
        bot = BotBarbarzynca(command_prefix="!")
        bot.run(
            settings["DISCORD_BOT_TOKEN"],
            log_handler=self.bot_log_handler,
            log_formatter=bot_log_format(),
        )
