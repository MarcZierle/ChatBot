import asyncio, logging, os

from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig

import settings, globals


class RasaModelHandler():

    loop = None

    def __init__(self, userid, model_path="./models"):
        self.__userid       = str(userid)
        self.__model_path   = model_path

        if not RasaModelHandler.loop:
            RasaModelHandler.loop = asyncio.get_event_loop()

        try:
            self.__agent = self.__restore_model()
        except Exception:
            self.__agent = self.__load_new_model()


    def __load_new_model(self):
        # _tracker_store = RedisTrackerStore(domain, host=os.environ["REDIS_HOST"])
        #
        # _agent = load_agent(cmdline_args.core,
        #              interpreter=_interpreter,
        #              tracker_store=_tracker_store,
        #              endpoints=_endpoints)
        return Agent.load(
            self.__model_path + "/basic_model",
            action_endpoint = EndpointConfig( url="http://localhost:5055/webhook" )
        )


    def __restore_model(self):
        return globals.restore_object(
            self.__model_path + "/stored_models/",
            self.__userid
        )


    @classmethod
    def remove_all_stored_models():
        pass


    def __store(self):
        # globals.store_object(
        #     self.__agent,
        #     self.__model_path + "/stored_models/",
        #     self.__userid
        # )
        #self.__agent.persist(self.__model_path + "/stored_models")
        pass


    async def __parse_agent(self, msg, userid):
        return await self.__agent.handle_text(msg, sender_id=userid)


    def parse(self, msg, userid):
        response = RasaModelHandler.loop.run_until_complete(self.__parse_agent(msg, userid))
        self.__store()
        return response



if __name__ == "__main__":
    settings.init()

    model = RasaModelHandler(userid="user_id_marc", model_path="rasa/models")

    userid_1 = 1234
    userid_2 = 9876

    print("Bot is ready!")
    # while True:
    #     msg = input()
    #     print("User: \t" + msg)
    #     print("Bot: \t" + str(model.parse(msg)))

    print("U1: hi")
    print("B : " + str(model.parse("hi", userid_1)))

    print("U1: yes")
    print("B : " + str(model.parse("yes", userid_1)))

    print("U1: bye")
    print("B : " + str(model.parse("bye", userid_1)))

    print("U1: hi")
    print("B : " + str(model.parse("hi", userid_1)))

    print("********** USER SWITCH **********")

    print("U2: hi")
    print("B : " + str(model.parse("hi", userid_2)))

    print("U2: yes")
    print("B : " + str(model.parse("yes", userid_2)))

    print("U2: hi")
    print("B : " + str(model.parse("hi", userid_2)))

    print("U2: hi")
    print("B : " + str(model.parse("hi", userid_2)))

    print("U2: hi")
    print("B : " + str(model.parse("hi", userid_2)))

    print("U2: hi")
    print("B : " + str(model.parse("hi", userid_2)))

    print("U2: bye")
    print("B : " + str(model.parse("bye", userid_2)))

    print("********** USER SWITCH **********")

    print("U1: yes")
    print("B : " + str(model.parse("yes", userid_1)))

    print("U1: bye")
    print("B : " + str(model.parse("bye", userid_1)))
