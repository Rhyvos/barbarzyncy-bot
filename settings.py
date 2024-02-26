import os
from dotenv import load_dotenv

load_dotenv()

def set_project_paths(env_file):
    project_root = os.path.abspath(os.path.dirname(__file__))
    log_dir = os.path.join(project_root, 'logs')
    db_dir = os.path.join(project_root, 'db')
    env_file.write(f'\nPROJECT_ROOT={project_root}')
    env_file.write(f'\nLOGS_DIR={log_dir}')
    env_file.write(f'\nDB_DIR={db_dir}')

def set_or_exchange_token(env_file, exchange_token=False):
    print("Getting token...")
    existing_token = os.environ.get('DISCORD_BOT_TOKEN')
    if not existing_token:
        user_token = input("Podaj token: ")
    elif exchange_token:
        change_token = input(f"Znalazłem już DISCORD_BOT_TOKEN={existing_token}. Czy chcesz zmienić token? (Y/N): ")
        if change_token.lower() == 'y' or change_token.lower() == 'yes':
            user_token = input("Podaj nowy token: ")
    else:
        user_token = existing_token
    env_file.write(f'\nDISCORD_BOT_TOKEN={user_token}')

def load_settings():
    print("Setting up environment...")
    
    with open('.env', 'w') as env_file:
        set_project_paths(env_file)
        set_or_exchange_token(env_file)