tg = telegram.Telegram( api_key=TELEGRAM_API_KEY )
tg.restore("./telgram/messages/")

rasa = rasa.RasaWrapper()
rasa.restore("./rasa/state")

while(bot_running):
    if tg.fetchnewmessages():
        for userid in tg.get_user_with_new_messages()
            thread.start_new_thread(tg.process_message, userid, rasa)

tg.save("./telegram/messages/")


def TelegramManager::process_message(self, userid, rasa):
    for msg in self.getnewmessages(userid):
        response, shouldsend = rasa.processMessage(userid, msg)

        if shouldsend:
            tg.sendmessage(userid, response)
