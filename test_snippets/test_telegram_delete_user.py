import os
from dotenv import load_dotenv
from pathlib import Path
import os, logging, atexit

from telegrammanager.telegrammanager import TelegramManager

TG_STORAGE_PATH     = fix_file_path("./storage/telegram/", True)
TG_CHATLOG_PATH     = fix_file_path("./storage/chatlogs/", True)
TG_DOWNLOADS_PATH   = fix_file_path("./storage/downloads/", True)

env_path = Path('/mnt/c/Users/Think Pad/Desktop/VirtualEnvChatBot/ChatBot') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

global TELEGRAM_API_KEY, GOOGLE_DISTANCE_MATRIX_API_KEY
GOOGLE_DISTANCE_MATRIX_API_KEY  = os.getenv("GOOGLE_DISTANCE_MATRIX_API_KEY")
TELEGRAM_API_KEY                = os.getenv("TELEGRAM_API_KEY")

global tel_man
tel_man = TelegramManager( api_key=TELEGRAM_API_KEY )

while True:
    tel_man.fetch_new_messages()
    print(tel_man.get_users())
    tel_man.delete_user(userid)
    print("User deleted\n\n")
    print(tel_man.get_users())


def fix_file_path(path, mkdir=False) :
        if os.name == "nt" :
            path = path.replace("/", "\\")
            #debug(path)
            #debug(os.name)
            debug("Fixed file path: " + path)
        if mkdir:
            os.makedirs(os.path.dirname(path),exist_ok=True)

            debug("created new directory with path: " + os.path.dirname(path))
        return path
