import datetime as dt, logging, time

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

planner = Scheduler(gdm_querent)

planner.add_day(25, 5, 2019)
planner.add_day(26, 5, 2019)
planner.add_day(27, 5, 2019)
planner.add_day(28, 5, 2019)

planner.add_event(Event(
    "Datenbanken Vorlesung",
    Event.EventType.SPECIFIC,
    Scheduler.to_minutes(11, 0),
    Scheduler.to_minutes(13, 0),
    place="Rudower Chaussee 25 Berlin"
), [27, 5, 2019])

planner.add_event(Event(
    "Datenbanken Übung",
    Event.EventType.SPECIFIC,
    Scheduler.to_minutes(11, 0),
    Scheduler.to_minutes(13, 0),
    place="Rudower Chaussee 25 Berlin"
), [28, 5, 2019])

planner.add_event(Event(
    "C++ Vorlesung",
    Event.EventType.SPECIFIC,
    Scheduler.to_minutes(13, 0),
    Scheduler.to_minutes(15, 0),
    place="Rudower Chaussee 26 Berlin"
), [28, 5, 2019])

planner.add_event(Event(
    "Datenbanken Vorlesung",
    Event.EventType.SPECIFIC,
    Scheduler.to_minutes(15, 0),
    Scheduler.to_minutes(17, 0),
    place="Rudower Chaussee 25 Berlin"
), [28, 5, 2019])

planner.add_event(Event(
    "Kuchenbacken",
    Event.EventType.UNSPECIFIC,
    duration = Scheduler.to_minutes(2, 30),
    place = "Str. d. Pariser Kommune 30"
))

exit()

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

while True:
    logging.debug("Fetching new messages...")
    tgm.fetchnewmessages()
    logging.debug("Fetching done!")

    logging.debug("Checking new messages...")
    for user in tgm.users:
        logging.debug("Checking new messages for user " + str(user))
        msgs = tgm.getnewmessages(user)

        if len(msgs) > 0:
            for msg in msgs:
                logging.debug("Processing message \"" + msg + "\"")

                response = simple_message_processing(user, msg)
                tgm.sendmessage(user, response)

        logging.debug("User messages done! [" + str(user) + "]")

    logging.debug("Checking done!")
