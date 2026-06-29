from dotenv import load_dotenv
import os

load_dotenv()


def get_database_url() -> str:
    return os.getenv('DATABASE_URL', 'sqlite:///./taskflow.db')
