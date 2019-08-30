import os
import datetime as dt
import logging
import time
import iso8601

#from rasa.core.agent import Agent
#from rasa.core.interpreter import RasaNLUInterpreter

from planner import plannerhandler as ph

import settings
import globals
settings.init()

from settings import tel_man, rasa_model

survey_link = "https://forms.gle/1doFP9G4LbG83cuH9"


remove_event_for_user_on_day = {}


chat_save_it = 0
while True:
#    try:
    globals.debug('Fetching new messages...')
    if not tel_man.fetch_new_messages():
        globals.debug('Fetching failed.')
        continue
    globals.debug('Fetching done!')

    globals.debug('Checking new messages...')
    for userid in tel_man.get_users():
        globals.debug('Checking new messages for user '
                      + str(userid))
        msgs = tel_man.get_new_messages(userid)
        files = tel_man.get_new_files(userid)
        callback_queries = tel_man.get_new_callback_queries(userid)

        if msgs:
            for msg in msgs:

                if "/stop" in msg:
                    if str(userid) == "521748695" or str(userid) == "127069982":
                        tel_man.send_message(userid,"Aye captain! Ye olde server will be stopped.")
                        exit()
                    else:
                        tel_man.send_message(userid,"No permissions for stopping the server!")
                        continue

                if "/feedback" in msg:
                    tel_man.send_message(userid,
                        "If you are feeling comfortable using JANUS and think, "
                        + "you have seen everything there is, then be sure to complete "
                        + "our survey on your chatting experience:\n"
                        + survey_link + "\n"
                        + "Thank you!")
                    continue

                if "/help" in msg:
                    tel_man.send_message(userid,
                        "Here is small list of everything I can do for you:\n"
                        + "• Plan an event at a specific location and time %26 date or duration. "
                        + "If you don't know the exact time and date an event should be scheduled, you can just "
                        + "give JANUS the duration of how long you expect it to take.\n"
                        + "(e.g. \"Plan an event at [address].\")\n"
                        + "• Show your scheduled events.\n"
                        + "(e.g. \"What has been scheduled?\")\n"
                        + "• Remove a planned event from your schedule.\n"
                        + "(e.g. \"Cancel an event.\")\n"
                        + "• Giving /feedback\n"
                        + "• /cancel to reset the current conversation state.")
                    continue

                if "/cancel" in msg:
                    msg = "/reset_conversation"
                elif tel_man.is_user_new(userid):
                    msg = "/introduction"


                response = rasa_model.parse(userid, msg)

                for resp_text in response:
                    resp_text = resp_text['text']

                    if "/show_plan" in resp_text:
                        globals.debug('sending plan image to user')
                        os.system("cp storage/schedule_images/"+str(userid)+".png storage/schedule_images/my_schedule.png")
                        tel_man.send_file(userid, "storage/schedule_images/my_schedule.png")
                        continue

                    if "/remove_event" in resp_text:
                        _, time_stamp = resp_text.split("/remove_event",1)
                        time_stamp = iso8601.parse_date(time_stamp)

                        globals.debug('user wants to delete an event on day ' + str(time_stamp))

                        planner = ph.restore("storage/schedules/", userid)
                        event_names = planner.get_day_event_names(time_stamp.day, time_stamp.month, time_stamp.year)

                        if event_names:
                            tel_man.send_message(userid, 'Which event do you want me to delete?', event_names + ["Cancel"])
                            remove_event_for_user_on_day[userid] = (time_stamp, len(event_names))
                        else:
                            tel_man.send_message(userid,
                                'Nothing is planned on '
                                + time_stamp.strftime("%A") + ', ' + time_stamp.strftime("%d.%m.%y") + '.')

                        continue

                    tel_man.send_message(userid, resp_text)

        globals.debug('Messages done for user ' + str(userid))

        if callback_queries:
            for callback_query in callback_queries:
                callback_query_id = callback_query[0]
                callback_answer = int(callback_query[1])

                tel_man.answer_callback_query(callback_query_id, "Checked!")

                time_stamp = remove_event_for_user_on_day[userid][0]
                cancel_bt = remove_event_for_user_on_day[userid][1]

                if callback_answer < cancel_bt:
                    planner = ph.restore("storage/schedules/", userid)
                    event_name = planner.remove_event_from_day(
                        time_stamp.day,time_stamp.month,time_stamp.year,
                        int(callback_answer))
                    ph.store("storage/schedules/", userid, planner)
                    tel_man.send_message(userid,"Alright, I removed " + event_name
                        + " from " + time_stamp.strftime("%A") + ', ' + time_stamp.strftime("%d.%m.%y") + '.')
                else:
                    tel_man.send_message(userid,"No problem :)")

        if files:
            for file in files:
                tel_man.send_message(userid, 'Saving your file...')
                globals.debug('Processing file "' + file[1]
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
