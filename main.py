import os, datetime as dt, logging, time

from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

# import telegram as tg
# from telegram import telegrammanager
# from telegram.telegrammanager import TelegramManager

import settings, globals
settings.init()

import asyncio


def parse(msg):
    agent = Agent.load("rasa/models")
    response = asyncio.run( agent.handle_text("hi") )
    return response

    # inter = Interpreter.load("rasa/models/")


if __name__ == "__main__":
    print(parse("hi"))
    print(parse("bye"))
