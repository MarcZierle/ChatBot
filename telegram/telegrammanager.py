import urllib.parse as up
import urllib.request as ur, json

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.api_key = api_key
        self.offset = 0
        self.timeout = 100
        self.allowed_updates = "message"

        self.users = []
        self.user_status = {}
        self.user_messages = {}


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
        response = json.loads(ur.urlopen(self.__build_getupdates_url()).read().decode('utf-8'))
        #print(json.dumps(response, sort_keys=True, indent=4))
        #response_list = []
        for message in response["result"] :
            if "text" in message["message"] :
                uid = message["message"]["from"]["id"]
                txt = message["message"]["text"]
                if uid in self.user_messages :
                    self.user_messages[uid].append(txt)
                else :
                    self.user_messages[uid] = [txt]
                    self.users.append(uid)
        if len(response["result"]) > 0 :
            self.offset = response["result"][-1]["update_id"] + 1
            #print(self.offset)
            if len(response["result"]) >= 99 :
                self.fetchnewmessages()

    def getnewmessages(self, userid):
        if userid in self.user_messages:
            msgs = self.user_messages[userid]
            self.user_messages[userid] = []
            return msgs
        return None

    def sendmessage(self, userid, msg):
        ur.urlopen(self.__build_sendmessage_url(userid, msg))

    def __get_user_status(self, userid):
        if userid in self.user_status :
            return self.user_status(userid)

    def __set_user_status(self, userid, status):
        self.user_status = status

    def __add_new_user(self, userid):
        if userid not in self.users :
            self.users.append(userid)

    def __get_next_message(self, userid):
        if userid in self.user_messages :
            if len(self.user_messages[userid]) > 0 :
                return self.user_messages[userid].pop(0)
