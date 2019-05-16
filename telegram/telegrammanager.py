import urllib.parse as up

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.api_key = api_key
        self.offset = 0
        self.timeout = 500

        self.users = {}
        self.user_status = {}
        self.user_messages = {}

        print(self.__build_url())


    def restore(self):
        return

    def __build_url(self):
        return up.quote((
            TelegramManager.base_url + self.api_key +
            "/getUpdates" +
            "?offset=" + str(self.offset) +
            "&timeout=" + str(self.timeout)
            ), safe='/:?&=.,+-_%|')

    def fetchnewmessages(self):
        return

    def getnewmessages(self):
        return

    def sendmessage(self, userid, msg):
        return

    def __get_user_status(self, userid):
        return

    def __set_user_status(self, userid, status):
        return

    def __add_new_user(self, userid):
        return

    def __get_next_message(self, userid):
        return
