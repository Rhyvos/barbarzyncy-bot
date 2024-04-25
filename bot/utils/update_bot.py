import git
import os
import subprocess

from bot_logger import bot_logger, log

from dotenv import load_dotenv

load_dotenv()

logger = bot_logger("update_bot")


def update_bot():
    logger.info("Starting bot update.")
    
    repo = git.Repo(os.getenv("PROJECT_ROOT"))
    origin = repo.remotes.origin
    origin.pull()

    requirements_path = os.path.join(os.getenv("PROJECT_ROOT"), "requirements.txt")
    # return run_command(f"pip install -U -r {requirements_path}")
    return "Success"


def check_for_updates():
    logger.info("Checking for updates...")
    try: 
        repo = git.Repo(os.getenv("PROJECT_ROOT"))
        origin = repo.remotes.origin
        origin.fetch()

        local_commit = repo.git.rev_parse("HEAD")
        remote_commit = repo.git.rev_parse("origin/master")
        if repo.git.rev_list(f"{local_commit}..{remote_commit}"):
            logger.info("Local repository is behind remote. Starting bot update.")
            ret = update_bot()
            return ret
        else:
            logger.info("Local repository is up-to-date with the remote.")
            return "No updates found."
    except Exception as e:
        return f"{e.__class__.__name__}: {str(e)}"

@log
def run_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, text=True, stderr=subprocess.STDOUT
        )
        return result
    except subprocess.CalledProcessError as e:
        return f"Command failed with error: {e.returncode}\n{e.output}"
