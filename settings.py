from dotenv import load_dotenv
from pathlib import Path
import os, logging

def init():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)

    global GOOGLE_DISTANCE_MATRIX_API_KEY, TELEGRAM_API_KEY
    GOOGLE_DISTANCE_MATRIX_API_KEY  = os.getenv("GOOGLE_DISTANCE_MATRIX_API_KEY")
    TELEGRAM_API_KEY                = os.getenv("TELEGRAM_API_KEY")

    logging.basicConfig(level=logging.DEBUG)
