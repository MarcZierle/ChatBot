# Download: pip install python-dotenv

import datetime as dt

import googledistancematrix as gdm
from googledistancematrix import querent
from googledistancematrix.querent import Querent

import telegram as tg
from telegram import telegrammanager
from telegram.telegrammanager import TelegramManager

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
#print(tgm.user_messages)


#print(tgm.getnewmessages())
#i = 1
#while(i < 5) :
#    tgm.sendmessage(
#    userid = "______",
#    msg = "."
#    )
#    time.sleep(1)
#    print(i)
#    i = i+1
    
