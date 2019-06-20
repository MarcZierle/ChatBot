from dotenv import load_dotenv
from pathlib import Path
import os, logging, atexit

def init():
    env_path = Path('/home/marc/University/Chatbot') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)
    #load_dotenv(".env", verbose=True)

    global GOOGLE_DISTANCE_MATRIX_API_KEY, TELEGRAM_API_KEY
    GOOGLE_DISTANCE_MATRIX_API_KEY  = os.getenv("GOOGLE_DISTANCE_MATRIX_API_KEY")
    TELEGRAM_API_KEY                = os.getenv("TELEGRAM_API_KEY")

    #logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('scheduler').setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    atexit.register(exit_handler)

def exit_handler():
    print ('Server exiting...')
