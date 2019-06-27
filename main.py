import os
import datetime as dt
import logging
import time

from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

from planner import plannerhandler as ph

import settings
import globals
settings.init()

from settings import tel_man, rasa_model

user_gave_event_name = {}


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
                if userid in user_gave_event_name.keys() and not user_gave_event_name[userid]:
                    response = rasa_model.parse(userid, msg)
                else:
                    logging.debug('this message is interpreted as an event name.')
                    user_gave_event_name[userid] = False
                    response = rasa_model.parse(userid, '/gives_event_name{"event_name":"'+msg+'"}')

                for resp_part in response:
                    resp_part = resp_part['text']
                    if "/show_plan" in resp_part:
                        logging.debug('sending plan image to user')
                        tel_man.send_file(userid, "storage/schedule_images/"+str(userid)+".png")
                        continue

                    if "/ask_event_name" in resp_part:
                        logging.debug('awaiting event name from user in next message.')
                        user_gave_event_name[userid] = True
                        resp_part = resp_part.replace("/ask_event_name", "", 1)

                    tel_man.send_message(userid, resp_part)

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

                    if ".ics" in file[1] or ".ical" in file[1]:
                        # add events to planner
                        planner = ph.restore("storage/schedules/", userid)
                        planner.import_ics(settings.TG_DOWNLOADS_PATH + str(userid)+ '/'+file[1])
                        ph.store("storage/schedules/", userid, planner)
                        response = response + '\nI added your events to your plan.'
                else:
                    response = "Sorry, but I couldn't save that."

                tel_man.send_message(userid, response)

    #except Exception as e:
#        logging.error(str(e))

    if chat_save_it % 5 == 0:
        tel_man.store_chatlog(settings.TG_CHATLOG_PATH)
    ++chat_save_it
