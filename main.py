import os
import datetime as dt
import logging
import time

#from rasa.core.agent import Agent
#from rasa.core.interpreter import RasaNLUInterpreter

#from planner import plannerhandler as ph

import settings
import globals
settings.init()

from settings import tel_man#, rasa_model

# ------ TESTING ----- #
tel_man.fetch_new_messages()
tel_man.send_message(127069982, "Does this work?",["Yes","No"])
tel_man.fetch_new_messages()
for callback_query in tel_man.get_new_callback_queries(127069982) :
    #you have to answer a callback_query so the clock icon disappears, don't know why the text stuff doesn't work
    tel_man.answer_callback_query(callback_query[0], "Okay, you answered: "+callback_query[1])
tel_man.store_chatlog(settings.TG_CHATLOG_PATH)
##chat_save_it = 0
##while True:
###    try:
##    logging.debug('Fetching new messages...')
##    if not tel_man.fetch_new_messages():
##        logging.debug('Fetching failed.')
##        continue
##    logging.debug('Fetching done!')
##
##    logging.debug('Checking new messages...')
##    for userid in tel_man.get_users():
##        logging.debug('Checking new messages for user '
##                      + str(userid))
##        msgs = tel_man.get_new_messages(userid)
##        files = tel_man.get_new_files(userid)
##
##        if msgs:
##            for msg in msgs:
##                response = rasa_model.parse(userid, msg)
##                for resp_part in response:
##                    if "/show_plan" in resp_part['text']:
##                        logging.debug('sending plan image to user')
##                        tel_man.send_file(userid, "storage/schedule_images/"+str(userid)+".png")
##                        continue
##
##                    tel_man.send_message(userid, resp_part['text'])
##
##        logging.debug('Messages done for user ' + str(userid))
##
##        if files:
##            for file in files:
##                tel_man.send_message(userid, 'Saving your file...')
##                logging.debug('Processing file "' + file[1]
##                              + '" with file_id "' + file[0] + '"')
##
##                if tel_man.get_file(file[0],
##                        settings.TG_DOWNLOADS_PATH + str(userid)
##                        + '/', file[1]):
##                    response = 'Alright, I got it!'
##
##                    if ".ics" in file[1] or ".ical" in file[1]:
##                        # add events to planner
##                        planner = ph.restore("storage/schedules/", userid)
##                        planner.import_ics(settings.TG_DOWNLOADS_PATH + str(userid)+ '/'+file[1])
##                        ph.store("storage/schedules/", userid, planner)
##                        response = response + '\nI added your events to your plan.'
##                else:
##                    response = "Sorry, but I couldn't save that."
##
##                tel_man.send_message(userid, response)
##
##    #except Exception as e:
###        logging.error(str(e))
##
##    if chat_save_it % 5 == 0:
##        tel_man.store_chatlog(settings.TG_CHATLOG_PATH)
##    ++chat_save_it
##
