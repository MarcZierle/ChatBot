import urllib.parse as up
import urllib.request as ur, json

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.api_key = api_key
        self.offset = 0
        self.timeout = 10
        self.allowed_updates = "message"

        self.users = {}
        self.user_status = {}
        self.user_messages = []

        self.getnewmessages()
        print("OK")
        print(self.__get_next_message(127069982))
        print("OK")
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
        return getnewmessages()

    def getnewmessages(self): 
        response = json.loads(ur.urlopen(self.__build_getupdates_url()).read())
        #print(json.dumps(response, sort_keys=True, indent=4))
        response_list = []
        for message in response["result"] :
            if "text" in message["message"] :
                new_element = {"userid":message["message"]["chat"]["id"],"message":message["message"]["text"]}
                response_list.append(new_element)
        if len(response["result"]) > 0 :
            self.offset = response["result"][-1]["update_id"] +1
        self.user_messages = response_list

    def sendmessage(self, userid, msg):
        ur.urlopen(self.__build_sendmessage_url(userid, msg))

    def __get_user_status(self, userid):
        if userid in self.user_status :
            return self.user_status(userid)

    def __set_user_status(self, userid, status):
        return

    def __add_new_user(self, userid):
        if userid not in self.users :
            self.users.append(userid)

    def __get_next_message(self, userid):
        #print(userid)
        #print(self.user_messages)
        #if userid in self.user_messages["userid"] :
        #    return self.user_messages[userid]
        #else :
        #    return "Nope"
        return
