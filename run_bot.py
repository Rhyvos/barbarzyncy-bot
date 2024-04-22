import django
import os
import sys
import asyncio


from django.conf import settings as project_settings
from dotenv import dotenv_values
from bot.utils.bot_logger import bot_log_handler, bot_log_format

DOTENV_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BarbarzyncyBot', '.env')
settings = dotenv_values(DOTENV_PATH)
sys.path.append(settings['DJANGO_ROOT'])

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BotManager.settings")
django.setup()

from bot.BotBarbarzynca import BotBarbarzynca

bot_log_handler = bot_log_handler()

bot = BotBarbarzynca(command_prefix="!")
bot.run(
    settings["DISCORD_BOT_TOKEN"],
    log_handler=bot_log_handler,
    log_formatter=bot_log_format(),
)

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'Barbarzyncy Discord bot healthcheck.\n'
    version = 'Python %s\n' % sys.version.split()[0]
    response = '\n'.join([message, version])
    return [response.encode()]
