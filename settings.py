from dotenv import load_dotenv
from pathlib import Path
import os, logging, atexit
import tensorflow as tf

from telegrammanager.telegrammanager import TelegramManager
from rasamodelhandler import RasaModelHandler

TG_STORAGE_PATH     = "./storage/telegram/"
TG_CHATLOG_PATH     = "./storage/chatlogs/"
TG_DOWNLOADS_PATH   = "./storage/downloads/"

RASA_MODEL_PATH     = "./rasa/models/basic_model/"


def init_api_keys():
    #env_path = Path('/home/marc/University/Chatbot') / '.env'
    #load_dotenv(dotenv_path=env_path, verbose=True)
    load_dotenv(".env", verbose=True)

    global GOOGLE_DISTANCE_MATRIX_API_KEY, TELEGRAM_API_KEY
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
    logging.debug("loading telegram manager...")
    global tel_man
    tel_man = TelegramManager( api_key=TELEGRAM_API_KEY )
    try:
        tel_man.restore(TG_STORAGE_PATH)
    except Exception:
        pass
    logging.debug("loading done!")

    # if possible restore RASA-Model
    logging.debug("loading rasa model...")
    global rasa_model
    rasa_model = RasaModelHandler(RASA_MODEL_PATH)
    logging.debug("loading done!")


def exit_handler():
    logging.debug("exiting server...")

    logging.debug("saving telegram chatlogs...")
    tel_man.store_chatlog(TG_CHATLOG_PATH)
    logging.debug("saving done!")

    logging.debug("saving telegram manager...")
    tel_man.store(TG_STORAGE_PATH)
    logging.debug("saving done!")

    logging.debug("exiting done!")
