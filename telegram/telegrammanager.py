import urllib.parse as up
import urllib.request as ur, json

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.api_key = api_key
        self.offset = 0
        self.timeout = 500
        self.allowed_updates = "message"

        self.users = {}
        self.user_status = {}
        self.user_messages = {}

        #print(self.getnewmessages())
        print(self.__build_getupdates_url())


    def restore(self):
        return

    def __build_getupdates_url(self):
        return up.quote((
            TelegramManager.base_url + self.api_key +
            "/getUpdates" +
            "?offset=" + str(self.offset) +
            "&timeout=" + str(self.timeout) +
            "&allowed_updates=" + self.allowed_updates
            ), safe='/:?&=.,+-_%|')

    def __build_sendmessage_url(self, userid, msg): 
        return up.quote(("https://api.telegram.org/bot"
                 + self.api_key
                 + "/sendMessage"
                 + "?chat_id=" + str(userid)
                 + "&text=" + msg
                  ), safe='/:?&=.,+-_%|')

    def fetchnewmessages(self):
        return

    def getnewmessages(self): 
        response = json.loads(ur.urlopen(self.__build_getupdates_url()).read())
        print(json.dumps(response, sort_keys=True, indent=4))
        response_list = []
        for message in response["result"] :
            if "text" in message["message"] :
                new_element = {message["message"]["chat"]["id"]:message["message"]["text"]}
                response_list.append(new_element)
        return response_list

    def sendmessage(self, userid, msg):
        #print(self.__build_sendmessage_url(userid, msg))
        ur.urlopen(self.__build_sendmessage_url(userid, msg))

    def __get_user_status(self, userid):
        if userid in self.user_status :
            return self.user_status(userid)

    def __set_user_status(self, userid, status):
        return

    def __add_new_user(self, userid):
        return

    def __get_next_message(self, userid):
        return
