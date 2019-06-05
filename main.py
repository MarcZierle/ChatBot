import datetime as dt, logging, time

import os

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import telegram as tg
from telegram import telegrammanager
from telegram.telegrammanager import TelegramManager

from planner import scheduler
from planner.scheduler import Scheduler
from planner.event import Event

import settings
settings.init()


gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.settravelmode(Querent.TravelMode.TRANSIT)

##planner = Scheduler(gdm_querent)
##
##planner.add_day(25, 5, 2019)
##planner.add_day(26, 5, 2019)
##planner.add_day(27, 5, 2019)
##planner.add_day(28, 5, 2019)
##
##planner.add_event(Event(
##    "Datenbanken Vorlesung",
##    Event.EventType.SPECIFIC,
##    Scheduler.to_minutes(11, 0),
##    Scheduler.to_minutes(13, 0),
##    place="Rudower Chaussee 25 Berlin"
##), [27, 5, 2019])
##
##planner.add_event(Event(
##    "Datenbanken Übung",
##    Event.EventType.SPECIFIC,
##    Scheduler.to_minutes(11, 0),
##    Scheduler.to_minutes(13, 0),
##    place="Rudower Chaussee 25 Berlin"
##), [28, 5, 2019])
##
##planner.add_event(Event(
##    "C++ Vorlesung",
##    Event.EventType.SPECIFIC,
##    Scheduler.to_minutes(13, 0),
##    Scheduler.to_minutes(15, 0),
##    place="Rudower Chaussee 26 Berlin"
##), [28, 5, 2019])
##
##planner.add_event(Event(
##    "Datenbanken Vorlesung",
##    Event.EventType.SPECIFIC,
##    Scheduler.to_minutes(15, 0),
##    Scheduler.to_minutes(17, 0),
##    place="Rudower Chaussee 25 Berlin"
##), [28, 5, 2019])
##
##planner.add_event(Event(
##    "Kuchenbacken",
##    Event.EventType.UNSPECIFIC,
##    duration = Scheduler.to_minutes(2, 30),
##    place = "Str. d. Pariser Kommune 30"
##))


#details = gdm_querent.gettraveldetails(
#    origins = ["Rudower Chaussee 25"],
#    destinations = ["Str. d. Pariser Kommune 30 Berlin"],
#    arrival_time = dt.datetime(2019, 5, 15, 20, 0)
#)

#print(details['rows'][0]['elements'][0]['duration']['text'])


def simple_message_processing(userid, msg):
    userid = str(userid)
    status = simple_message_processing.status
    origins = simple_message_processing.origins
    destinations = simple_message_processing.destinations

    if msg == "/reset":
        status[userid] = 0
        return "Ok. Chat for user " + userid + " reset."

    if userid not in status:
        status[userid] = 0

    if status[userid] == 0:
        response = "Hey there. Please enter a starting location."
        status[userid] = 1
    elif status[userid] == 1:
        origins[userid] = msg
        response = "Alright. Now your destination."
        status[userid] = 2
    else:
        destinations[userid] = msg
        travel_details = gdm_querent.gettraveldetails(
            origins = origins[userid],
            destinations = destinations[userid]
        )

        print (travel_details)

        ret_code = travel_details['rows'][0]['elements'][0]['status']
        if ret_code != "ZERO_RESULTS" and ret_code != "NOT_FOUND":
            time = travel_details['rows'][0]['elements'][0]['duration']['text']
            response = ("Very good. It will take you " + time + " from "
                        + travel_details['origin_addresses'][0] + " to "
                        + travel_details['destination_addresses'][0] + "."
                        + " You might now enter a next starting location.")
        else:
            response = ("Sorry. No routes could be found." +
                        " But feel free to enter a new starting location.")

        status[userid] = 1

    simple_message_processing.status = status
    simple_message_processing.origins = origins
    simple_message_processing.destinations = destinations

    return response

simple_message_processing.status = {}
simple_message_processing.origins = {}
simple_message_processing.destinations = {}



tgm = TelegramManager( api_key=settings.TELEGRAM_API_KEY )


##for x in range(0,2):
##    logging.debug("Fetching new messages...")
##    tgm.fetch_new_messages()
##    logging.debug("Fetching done!")
##
##    logging.debug("Checking new messages...")
##    for user in tgm.get_users() :
##        logging.debug("Checking new messages for user " + str(user))
##        msgs = tgm.get_new_messages(user)
##
##        if len(msgs) > 0:
##            for msg in msgs:
##                logging.debug("Processing message \"" + msg + "\"")
##                response = "OK"
##                #response = simple_message_processing(user, msg)
##                tgm.send_message(user, response)
##
##        logging.debug("User messages done! [" + str(user) + "]")
##
##    logging.debug("Checking done!")

# --- TESTING STUFF HERE ---    
tgm.fetch_new_messages()
#tgm.send_message(127069982,"test")
#tgm.send_photo(379480639,"IMG_8843_Focus.JPG")
#tgm.send_file(127069982,"test.txt")
#tgm.send_photo(127069982,"testphoto2.jpg")
#logging.debug("Photo sent.")
print(tgm.get_chatlog())

#path = os.getcwd()
#tlgr_storage_path = path + "/storage/telegram/"
#tgm.store(tlgr_storage_path)
#tgm.restore(tlgr_storage_path)


