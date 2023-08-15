import os
from dotenv import load_dotenv

def get_keys():
    load_dotenv()
    return os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASS"), os.getenv("DB_NAME")