# Download: pip install python-dotenv

import datetime as dt

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import telegram as tg
from telegram import telegrammanager
from telegram.telegrammanager import TelegramManager

import logging

import time

import settings
settings.init()


gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.settravelmode(Querent.TravelMode.TRANSIT)

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

        ret_code = travel_details['rows'][0]['elements'][0]['status']
        if ret_code != "ZERO_RESULTS" and ret_code != "NOT_FOUND":
            time = travel_details['rows'][0]['elements'][0]['duration']['text']
            response = ("Very good. It will take you " + time + " from "
                        + origins[userid] + " to " + destinations[userid] + "."
                        " You might now enter a next starting location.")
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


def simple_message_processing(userid, msg):
    return "Hello"
