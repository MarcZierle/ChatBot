import pickle
import os
import logging
import requests
import json
import hashlib
from datetime import datetime

import globals

class TelegramManager():

    base_url = ("https://api.telegram.org/bot")

    def __init__(self, api_key):
        self.__api_key = api_key
        self.__offset = 0
        self.__timeout = 100
        self.__allowed_updates = "message"

        self.__users            = {}        #{userid:("Name",Anonymous = False)}
        self.__user_status      = {}
        self.__user_messages    = {}
        self.__user_files       = {}
        self.__chatlog          = {}

    def restore(self, path):
        try :
            self.__offset           = globals.restore_object(path, "offset")
            self.__timeout          = globals.restore_object(path, "timeout")
            self.__allowed_updates  = globals.restore_object(path, "allowed_updates")
            self.__users            = globals.restore_object(path, "users")
            self.__user_status      = globals.restore_object(path, "user_status")
            self.__user_messages    = globals.restore_object(path, "user_messages")
            self.__user_files       = globals.restore_object(path, "user_files")
            self.__chatlog          = globals.restore_object(path, "chatlog")
        except Exception :
            logging.error("")

        #logging.debug(self.__user_messages)

    def store(self,path) :
        globals.store_object(self.__offset,             path, "offset")
        globals.store_object(self.__timeout,            path, "timeout")
        globals.store_object(self.__allowed_updates,    path, "allowed_updates")
        globals.store_object(self.__users,              path, "users")
        globals.store_object(self.__user_status,        path, "user_status")
        globals.store_object(self.__user_messages,      path, "user_messages")
        globals.store_object(self.__user_files,         path, "user_files")
        globals.store_object(self.__chatlog,            path, "chatlog")

    def __build_get_updates_url(self):
        return (
            TelegramManager.base_url + self.__api_key +
            "/getUpdates" +
            "?offset=" + str(self.__offset) +
            "&timeout=" + str(self.__timeout) +
            "&allowed_updates=" + self.__allowed_updates
            )

    def __build_send_message_url(self, userid, msg):
        return ("https://api.telegram.org/bot"
                 + self.__api_key
                 + "/sendMessage"
                 + "?chat_id=" + str(userid)
                 + "&text=" + msg
                  )

    def __build_send_file_url(self, userid) :
        return ("https://api.telegram.org/bot"
                 + self.__api_key
                 + "/sendDocument"
                 + "?chat_id=" + str(userid))

    def __build_send_photo_url(self, userid) :
        return ("https://api.telegram.org/bot"
                 + self.__api_key
                 + "/sendPhoto"
                 + "?chat_id=" + str(userid))

    def __build_get_file_url(self, fileid) :
        return ("https://api.telegram.org/bot"
                 + self.__api_key
                 + "/getFile"
                 + "?file_id=" + str(fileid))

    def __build_download_file_url(self, filepath) :
        return ("https://api.telegram.org/file/bot"
                 + self.__api_key
                 + "/"
                 + filepath)

    def fetch_new_messages(self):
        response = (requests.get(self.__build_get_updates_url())).json()
        #print(json.dumps(response, sort_keys=True, indent=4))
        for message in response["result"] :
            if "message" in message:
                if response["ok"] == False :
                    logging.debug(response["description"])
                    return False
                if "text" in message["message"] :
                    uid = message["message"]["from"]["id"]
                    txt = message["message"]["text"]
                    time= message["message"]["date"]+7200
                    user_name = message["message"]["from"]["first_name"]
                    if "last_name" in message["message"]["from"] :
                        user_name = user_name + " " + message["message"]["from"]["last_name"]
                    if uid in self.__user_messages :
                        self.__user_messages[uid].append(txt)
                        self.__chatlog[uid].append(time)
                        self.__chatlog[uid].append(u"\u03FF"+ txt)
                    else :
                        self.__user_messages[uid] = [txt]
                        self.__chatlog[uid] = [time]
                        self.__chatlog[uid].append(u"\u03FF"+ txt)
                        self.__users[uid] = (user_name, False)

                elif "document" in message["message"] :
                    uid     = message["message"]["from"]["id"]
                    fileid  = message["message"]["document"]["file_id"]
                    filename= message["message"]["document"]["file_name"]
                    time= message["message"]["date"]+7200
                    user_name = message["message"]["from"]["first_name"]
                    if "last_name" in message["message"]["from"] :
                        user_name = user_name + " " + message["message"]["from"]["last_name"]
                    if uid in self.__user_files :
                        self.__user_files[uid].append((fileid, filename))
                        self.__chatlog[uid].append(time)
                        self.__chatlog[uid].append(u"\u03FF"+ "[File with name " + filename + " sent.]")
                    else :
                        self.__user_files[uid] = [(fileid, filename)]
                        self.__chatlog[uid] = [time]
                        self.__chatlog[uid].append(u"\u03FF"+ "[File with name " + filename + " sent.]")
                        self.__users[uid] = (user_name, False)

        if len(response["result"]) > 0 :
            self.__offset = response["result"][-1]["update_id"] + 1
            if len(response["result"]) >= 99 :
                self.fetch_new_messages()
        return True

    def get_new_messages(self, userid):
        if userid in self.__user_messages:
            msgs = self.__user_messages[userid]
            self.__user_messages[userid] = []
            return msgs
        return None

    def get_new_files(self, userid) :
        if userid in self.__user_files :
            files = self.__user_files[userid]
            self.__user_files[userid] = []
            return files
        return None

    def send_message(self, userid, msg):
        url = self.__build_send_message_url(userid, msg)
        response = requests.post(url)
        if response.status_code == 200 :
            current_time = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())   #strftime('%Y-%m-%d %H:%M:%S')
            self.__chatlog[userid].append(current_time)
            self.__chatlog[userid].append(u"\u037D" + msg)


    def send_file(self, userid, filepath) :
        url = self.__build_send_file_url(userid)
        files = {"document":open(filepath,"rb")}
        requests.post(url,files = files)


    def send_photo(self, userid, filepath) :
        url = self.__build_send_photo_url(userid)
        files = {"photo":open(filepath,"rb")}
        requests.post(url,files = files).json

    def get_file(self, fileid, path, filename) :
        url = self.__build_get_file_url(fileid)
        response = requests.get(url).json()
        print(json.dumps(response, sort_keys=True, indent=4))
        if response["ok"] == False :
            logging.debug(response["description"])
            return False
        telegram_file_path = response["result"]["file_path"]
        url_download = self.__build_download_file_url(telegram_file_path)
        response = requests.get(url_download)
        filepath = globals.fix_file_path(path, mkdir=True)
        open(path + filename, "wb").write(response.content)
        return True

    def get_users(self) :
        return list(self.__users.keys())

    def get_username(self, userid) :
        return self.__users[userid][0]

    def get_chatlog(self) :
        return self.__chatlog

    def store_chatlog(self,path) :
        path = globals.fix_file_path(path, mkdir=True)
        for userid in self.__chatlog :
            if self.__users[userid][1] == False :
                f = open(path + str(userid) + ".txt","a+")
            else :
                f = open(path + self.__hash_user(userid) + ".txt","a+")
            for time_or_message in self.__chatlog[userid] :
                time_or_message = str(time_or_message)
                if time_or_message[0] == u"\u03FF" :
                    if self.__users[userid][1] == False :
                        f.write(self.__users[userid][0] + ": " + time_or_message[1:] + "\n")
                    else :
                        f.write("User: " + time_or_message[1:] + "\n")
                elif time_or_message[0] == u"\u037D" :
                    f.write("Chatbot: \t\t\t" + time_or_message[1:] + "\n")
                else :
                    time_or_message = datetime.utcfromtimestamp(int(time_or_message)).strftime('%Y-%m-%d %H:%M:%S')
                    f.write("[" + time_or_message + "] ")
            f.close()
        self.__chatlog = self.__chatlog.fromkeys(self.__chatlog, [])

    def __get_user_status(self, userid):
        if userid in self.__user_status :
            return self.__user_status(userid)

    def __set_user_status(self, userid, status):
        self.__user_status = status

##    def __add_new_user(self, userid):
##        if userid not in self.__users :
##            self.__users.append(userid)


    def __get_next_message(self, userid):
        if userid in self.__user_messages :
            if len(self.__user_messages[userid]) > 0 :
                return self.__user_messages[userid].pop(0)

    def set_anonymous_state(self, userid, state) :
        self.__users[userid] = (self.get_username(userid),state)

    def __hash_user(self, userid) :
        s = (str(userid)+self.get_username(userid)).encode()
        return hashlib.md5(s).hexdigest()

    def __has_duplicate_hash(self) :
        seen = set()
        for userid in self.__users :
            h = self.__hash_user(userid)
            if h in seen :
                return True
            seen.add(h)
        return False