from dotenv import load_dotenv
from pathlib import Path
import os, logging, atexit
import tensorflow as tf

import globals
from globals import fix_file_path

from telegrammanager.telegrammanager import TelegramManager
from rasamodelhandler import RasaModelHandler

TG_STORAGE_PATH     = "./ChatBot/storage/telegram/"
TG_CHATLOG_PATH     = "./ChatBot/storage/chatlogs/"
TG_DOWNLOADS_PATH   = "./ChatBot/storage/downloads/"

RASA_MODEL_PATH     = "./ChatBot/rasa/models/basic_model/"


def init_api_keys():
    #env_path = Path('/home/marc/University/Chatbot') / '.env'
    #load_dotenv(dotenv_path=env_path, verbose=True)
    load_dotenv("./ChatBot/.env", verbose=True)

    global TELEGRAM_API_KEY, GOOGLE_DISTANCE_MATRIX_API_KEY
    GOOGLE_DISTANCE_MATRIX_API_KEY  = os.getenv("GOOGLE_DISTANCE_MATRIX_API_KEY")
    TELEGRAM_API_KEY                = os.getenv("TELEGRAM_API_KEY")


def init():
    init_api_keys()

    # surpress TensorFlow Warnings
    tf.logging.set_verbosity(tf.logging.FATAL)
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("planner").setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("rasa").setLevel(logging.INFO)
    atexit.register(exit_handler)

    # if possible restore TelegramManager state
    globals.debug("loading telegram manager...")
    global tel_man
    tel_man = TelegramManager( api_key=TELEGRAM_API_KEY )
    try:
        tel_man.restore(TG_STORAGE_PATH)
    except Exception:
        pass
    globals.debug("loading done!")

    # if possible restore RASA-Model
    globals.debug("loading rasa model...")
    global rasa_model
    rasa_model = RasaModelHandler(RASA_MODEL_PATH)
    globals.debug("loading done!")


def exit_handler():
    globals.debug("exiting server...")

    globals.debug("saving telegram chatlogs...")
    tel_man.store_chatlog(TG_CHATLOG_PATH)
    globals.debug("saving done!")

    globals.debug("saving telegram manager...")
    tel_man.store(TG_STORAGE_PATH)
    globals.debug("saving done!")

    globals.debug("exiting done!")
