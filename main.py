import os
import datetime as dt
import logging
import time

from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

import settings
import globals
settings.init()

from settings import tel_man, rasa_model

chat_save_it = 0
while True:
#    try:
    logging.debug('Fetching new messages...')
    if not tel_man.fetch_new_messages():
        logging.debug('Fetching failed.')
        continue
    logging.debug('Fetching done!')

    logging.debug('Checking new messages...')
    for userid in tel_man.get_users():
        logging.debug('Checking new messages for user '
                      + str(userid))
        msgs = tel_man.get_new_messages(userid)
        files = tel_man.get_new_files(userid)

        if msgs:
            for msg in msgs:
                if len(msg) < 50:
                    logging.debug('Processing message "' + msg + '"'
                            )
                else:
                    logging.debug('Processing message "' + msg[:50]
                            + '"')

                response = rasa_model.parse(userid, msg)
                for resp_part in response:
                    tel_man.send_message(userid, resp_part['text'])

        logging.debug('Messages done for user ' + str(userid))

        if files:
            for file in files:
                tel_man.send_message(userid, 'Saving your file...')
                logging.debug('Processing file "' + file[1]
                              + '" with file_id "' + file[0] + '"')

                if tel_man.get_file(file[0],
                        settings.TG_DOWNLOADS_PATH + str(userid)
                        + '/', file[1]):
                    response = 'Alright, I got it!'
                else:
                    response = "Sorry, but I couldn't save that."

                tel_man.send_message(userid, response)

    #except Exception as e:
#        logging.error(str(e))

    if chat_save_it % 5 == 0:
        tel_man.store_chatlog(settings.TG_CHATLOG_PATH)
    ++chat_save_it
