import logging
import os
from dotenv import load_dotenv

load_dotenv()

def bot_logger(prefix=""):
    logs_dir = os.environ.get('LOGS_DIR')
    if logs_dir is not None and not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    elif logs_dir is None:
        logs_dir = ''
    
    log_file = os.path.join(logs_dir, 'bot_status.log')

    formatter = logging.Formatter(f"%(asctime)s [%(levelname)s] [%(name)s] %(message)s")

    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(prefix)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger

def log(func):
    def wrapper(*args, **kwargs):
        logger = bot_logger(func.__name__)
        logger.info(f"Function {func.__name__} is about to be called. Args: {args}, Kwargs: {kwargs}.")
        result = func(*args, **kwargs)
        logger.info(f"Function {func.__name__} has been called with result: {result}.")
        return result
    return wrapper
