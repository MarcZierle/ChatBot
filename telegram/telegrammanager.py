import urllib.parse as up
import urllib.request as ur, json
import pickle
import os
import logging

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__offset = 0
        self.__timeout = 100
        self.__allowed_updates = "message"

        self.__users = []
        self.__user_status = {}
        self.__user_messages = {}


    def restore(self, path):
        logging.debug(self.__user_messages)
        self.__user_messages= {}
        if os.name == "nt" :
            path = path.replace("/", "\\")
            logging.debug(path)
            logging.debug(os.name)
            
        try :
            self.__offset = pickle.load(open(path + "offset.pkl","rb"))
            self.__timeout = pickle.load(open(path + "timeout.pkl","rb"))
            self.__allowed_updates = pickle.load(open(path + "allowed_updates.pkl","rb"))
            self.__users = pickle.load(open(path + "users.pkl","rb"))
            self.__user_status = pickle.load(open(path + "user_status.pkl","rb"))
            self.__user_messages = pickle.load(open(path + "user_messages.pkl","rb"))
        except FileNotFoundError :
            logging.error("Telegram Manager: Restore File or Folder not found. Your path: \n" + path) 
            exit()
    

        logging.debug(self.__user_messages)

    def store(self,path) :
        if os.name == "nt" :
            path = path.replace("/", "\\")
            logging.debug(path)
            logging.debug(os.name)
            

        if not os.path.exists(path):
            os.makedirs(path)
            
        pickle.dump(self.__offset, open(path + "offset.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.__timeout, open(path + "timeout.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.__allowed_updates, open(path + "allowed_updates.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.__users, open(path + "users.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.__user_status, open(path + "user_status.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.__user_messages, open(path + "user_messages.pkl", "wb"),protocol=pickle.HIGHEST_PROTOCOL)
        
    def __build_get_updates_url(self):
        return up.quote((
            TelegramManager.base_url + self.__api_key +
            "/getUpdates" +
            "?offset=" + str(self.__offset) +
            "&timeout=" + str(self.__timeout) +
            "&allowed_updates=" + self.__allowed_updates
            ), safe='/:?&=.,+-_%|')

    def __build_send_message_url(self, userid, msg):
        return up.quote(("https://api.telegram.org/bot"
                 + self.__api_key
                 + "/sendMessage"
                 + "?chat_id=" + str(userid)
                 + "&text=" + msg
                  ), safe='/:?&=.,+-_%|')
##    def __build_send_file_url(userid, filepath) :
##        return up.quote(("https://api.telegram.org/bot"
##                 + self.__api_key
##                 + "/sendDocument"
##                 + "?chat_id=" + str(userid)
##                 + "&document=Content-Disposition: file; filename=\"" + filepath + "\""
##                 + "Content-Type: image/gifContent-Transfer-Encoding: binary
        


    def fetch_new_messages(self):
        response = json.loads(ur.urlopen(self.__build_get_updates_url()).read().decode('utf-8'))
        #print(json.dumps(response, sort_keys=True, indent=4))
        #response_list = []
        for message in response["result"] :
            if "text" in message["message"] :
                uid = message["message"]["from"]["id"]
                txt = message["message"]["text"]
                if uid in self.__user_messages :
                    self.__user_messages[uid].append(txt)
                else :
                    self.__user_messages[uid] = [txt]
                    self.__users.append(uid)
        if len(response["result"]) > 0 :
            self.__offset = response["result"][-1]["update_id"] + 1
            #print(self.__offset)
            if len(response["result"]) >= 99 :
                self.fetch_new_messages()

    def get_new_messages(self, userid):
        if userid in self.__user_messages:
            msgs = self.__user_messages[userid]
            self.__user_messages[userid] = []
            return msgs
        return None

    def send_message(self, userid, msg):
        url = self.__build_send_message_url(userid, msg)
        ur.urlopen(url)

    def send_file(self, userid, filepath) :
        url = self.__build_send_file_url(userid, filepath)
        ur.urlopen(url)
                                         
    def get_users(self) :
        return self.__users

    def __get_user_status(self, userid):
        if userid in self.__user_status :
            return self.__user_status(userid)

    def __set_user_status(self, userid, status):
        self.__user_status = status

    def __add_new_user(self, userid):
        if userid not in self.__users :
            self.__users.append(userid)

    def __get_next_message(self, userid):
        if userid in self.__user_messages :
            if len(self.__user_messages[userid]) > 0 :
                return self.__user_messages[userid].pop(0)
