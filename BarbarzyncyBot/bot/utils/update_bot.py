import git
import os
import schedule
import subprocess
import time

from bot_logger import bot_logger, log
from check_bot_health import reset

logger = bot_logger("update_bot")

def update_bot():
    logger.info("Starting bot update.")

    repo = git.Repo(os.getcwd())
    origin = repo.remotes.origin
    origin.pull()

    run_command("pip install -U -r requirements.txt") 
    reset()

    logger.info("Bot update completed successfully.")

def check_for_updates():
    logger.info("Checking for updates...")
    repo = git.Repo(os.getcwd())
    origin = repo.remotes.origin
    origin.fetch()

    local_commit = repo.git.rev_parse("HEAD")
    remote_commit = repo.git.rev_parse("origin/master")
    if repo.git.rev_list(f"{local_commit}..{remote_commit}"):
        logger.info("Local repository is behind remote. Starting bot update.")
        update_bot()
    else:
        logger.info("Local repository is up-to-date with the remote.")

@log
def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.returncode}\n{e.output}"


if __name__ == "__main__":
    schedule.every(1).seconds.do(check_for_updates)
    while True:
        schedule.run_pending()
        time.sleep(1)
