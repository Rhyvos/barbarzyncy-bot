from settings import load_settings
from setup_database import create_database

if __name__ == "__main__":
    load_settings()
    create_database()
