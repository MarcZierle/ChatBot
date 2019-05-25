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

#gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
#gdm_querent.settravelmode(Querent.TravelMode.TRANSIT)

#details = gdm_querent.gettraveldetails(
#    origins = ["Rudower Chaussee 25"],
#    destinations = ["Str. d. Pariser Kommune 30 Berlin"],
#    arrival_time = dt.datetime(2019, 5, 15, 20, 0)
#)

#print(details['rows'][0]['elements'][0]['duration']['text'])

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
                # process msg in new thread if status is IDLE
                tgm.sendmessage(user, "Hello, human.")

        logging.debug("User messages done! [" + str(user) + "]")

    logging.debug("Checking done!")
