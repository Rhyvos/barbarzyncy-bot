import os
from dotenv import load_dotenv, dotenv_values


DOTENV_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BarbarzyncyBot', '.env')

load_dotenv(DOTENV_PATH)


def set_project_paths(settings):
    project_root = os.path.abspath(os.path.dirname(__file__))
    django_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'BarbarzyncyBot')
    log_dir = os.path.join(django_root, 'logs')
    db_dir = os.path.join(django_root, 'db')
    bot_dir = os.path.join(django_root, 'bot')
    bot_path = os.path.join(bot_dir, 'barbarzyncy_bot.py')
    requirements_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'requirements.txt')

    settings['PROJECT_ROOT']=project_root
    settings['DJANGO_ROOT']=django_root
    settings['LOGS_DIR']=log_dir
    settings['DB_DIR']=db_dir
    settings['BOT_DIR']=bot_dir
    settings['BOT_PATH']=bot_path
    settings['REQUIREMENTS_PATH']=requirements_path

def set_or_exchange(settings, name):
    print(f"Getting {name}...")
    existing_value = os.environ.get(name)
    if existing_value:
        change_value = input(f"Znalazłem już {name}={existing_value}. Czy chcesz zmienić? (Y/N): ")
        if change_value.lower() == 'y' or change_value.lower() == 'yes':
            value = input(f"Podaj nowy {name}: ")
        else:
            value = existing_value
    else:
        value = input(f"Podaj {name}: ")
        value = existing_value
    settings[name]=value

def load_settings():
    print("Setting up environment...")
    settings = dotenv_values(DOTENV_PATH)
    set_project_paths(settings)
    set_or_exchange(settings, 'SECRET_KEY')
    with open(DOTENV_PATH, 'w') as env_file:
        for key, value in settings.items():
            env_file.write(f'{key}={value}\n')
            os.environ[key] = value
        