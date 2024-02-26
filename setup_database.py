import os
import sqlite3
from dotenv import load_dotenv
from bot.utils.bot_logger import bot_logger



def create_database():
    load_dotenv()
    logger = bot_logger("setup_database")
    logger.info("Setting up database...")
    db_dir = os.environ.get('DB_DIR')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db_file = os.path.join(db_dir, 'bot.db')

    if os.path.exists(db_file):
        logger.info('bot.db exists, skipping creation...')
        return
    else:
        logger.info('bot.db does not exist, creating new...')


    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requirement_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL
        )
    ''')

    # Tabela answer_type
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS answer_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL
        )
    ''')

    # Tabela questions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_type_id INTEGER,
            question_text TEXT NOT NULL,
            answer_type_id INTEGER,
            enabled INTEGER,
            FOREIGN KEY (requirement_type_id) REFERENCES requirement_type(id),
            FOREIGN KEY (answer_type_id) REFERENCES answer_type(id)
        )
    ''')
    connection.commit()
    connection.close()