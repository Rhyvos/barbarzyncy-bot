import os
from dotenv import load_dotenv


DOTENV_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BarbarzyncyBot', '.env')

load_dotenv(DOTENV_PATH)

def set_project_paths(env_file):
    project_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BarbarzyncyBot')
    log_dir = os.path.join(project_root, 'logs')
    db_dir = os.path.join(project_root, 'db')
    bot_dir = os.path.join(project_root, 'bot')
    bot_path = os.path.join(bot_dir, 'barbarzyncy_bot.py')
    requirements_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')

    env_file.write(f'\nPROJECT_ROOT={project_root}')
    env_file.write(f'\nLOGS_DIR={log_dir}')
    env_file.write(f'\nDB_DIR={db_dir}')
    env_file.write(f'\nBOT_DIR={bot_dir}')
    env_file.write(f'\nBOT_PATH={bot_path}')
    env_file.write(f'\nREQUIREMENTS_PATH={requirements_path}')

def set_or_exchange(env_file, name):
    print("Getting {name}...")
    existing_token = os.environ.get(name)
    if not existing_token:
        user_token = input("Podaj {name}: ")
        change_token = input(f"Znalazłem już {name}={existing_token}. Czy chcesz zmienić? (Y/N): ")
        if change_token.lower() == 'y' or change_token.lower() == 'yes':
            user_token = input("Podaj nowy {name}: ")
    else:
        user_token = existing_token
    env_file.write(f'\nDISCORD_BOT_TOKEN={user_token}')

def load_settings():
    print("Setting up environment...")
    
    with open(DOTENV_PATH, 'w') as env_file:
        set_project_paths(env_file)
        set_or_exchange(env_file, 'SECRET_KEY')