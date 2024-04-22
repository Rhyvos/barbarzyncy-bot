import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def bot_log_format():
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    return logging.Formatter(
        "[{asctime}] [{levelname:<8}] [{name}]: {message}", dt_fmt, style="{"
    )


def bot_log_handler():
    logs_dir = os.environ.get("LOGS_DIR")
    if logs_dir is not None and not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    elif logs_dir is None:
        logs_dir = ""

    log_file = os.path.join(logs_dir, "bot_status.log")

    return logging.FileHandler(filename=log_file, encoding="utf-8", mode="a")


def bot_logger(prefix=""):
    formatter = bot_log_format()

    file_handler = bot_log_handler()
    file_handler.setFormatter(formatter)
    # std_handler = logging.StreamHandler(sys.stdout)
    # std_handler.setFormatter(formatter)
    # std_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(prefix)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    # logger.addHandler(std_handler)

    return logger


def log(func):
    def wrapper(*args, **kwargs):
        logger = bot_logger(func.__name__)
        logger.info(
            f"Function {func.__name__} is about to be called. Args: {args}, Kwargs: {kwargs}."
        )
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} has been called with result: {result}.")
        return result

    return wrapper
