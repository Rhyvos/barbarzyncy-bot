import git
import os
import schedule
import subprocess
import time

from bot_logger import bot_logger, log
from check_bot_health import reset

logger = bot_logger("update_bot")

def update_bot():
    """Pull the latest changes from the git repository, update packages, and restart the bot service."""
    logger.info("Starting bot update.")

    repo = git.Repo(os.getcwd())
    origin = repo.remotes.origin
    origin.pull()

    run_command("pip install -U -r requirements.txt") 
    reset()

    logger.info("Bot update completed successfully.")

def check_for_updates():
    """Check the repository for new commits and trigger bot update if necessary."""
    logger.info("Checking for updates...")
    repo = git.Repo(os.getcwd())
    origin = repo.remotes.origin
    origin.fetch()

    local_commit = repo.commit()
    remote_commit = origin.refs.master.commit
    if local_commit != remote_commit:
        logger.info("New commits found. Starting bot update.")
        update_bot()
    else:
        logger.info("No new commits.")

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
