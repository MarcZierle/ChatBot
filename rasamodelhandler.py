import asyncio, logging, os

from rasa.core.agent import Agent
from rasa.utils.endpoints import EndpointConfig

import settings, globals


class RasaModelHandler():

    loop = None

    def __init__(self, model_path="./ChatBot/rasa/models/basic_model"):
        self.__model_path   = model_path

        if not RasaModelHandler.loop:
            RasaModelHandler.loop = asyncio.get_event_loop()

        self.__agent = self.__load_model()


    def __load_model(self):
        # TODO: connect to DB using TrackerStore (and SQL?)
        # _tracker_store = RedisTrackerStore(domain, host=os.environ["REDIS_HOST"])
        #
        # _agent = load_agent(cmdline_args.core,
        #              interpreter=_interpreter,
        #              tracker_store=_tracker_store,
        #              endpoints=_endpoints)
        return Agent.load(
            self.__model_path,
            action_endpoint = EndpointConfig( url="http://localhost:5055/webhook" )
        )


    async def __parse_agent(self, sender_id, msg):
        return await self.__agent.handle_text(msg, sender_id=sender_id)


    def parse(self, sender_id, msg):
        return RasaModelHandler.loop.run_until_complete(self.__parse_agent(sender_id, msg))



if __name__ == "__main__":
    settings.init()

    model = RasaModelHandler(userid="user_id_marc", model_path="rasa/models")

    userid_1 = 1234
    userid_2 = 9876

    print("Bot is ready!")
    while True:
        msg = input()
        print("User: \t" + msg)
        print("Bot: \t" + str(model.parse(msg, 1)))

    exit()

    print("U1: hi")
    print("B : " + str(model.parse(userid_1, "hi")))

    print("U1: yes")
    print("B : " + str(model.parse(userid_1, "yes")))

    print("U1: bye")
    print("B : " + str(model.parse(userid_1, "bye")))

    print("U1: hi")
    print("B : " + str(model.parse(userid_1, "hi")))

    print("********** USER SWITCH **********")

    print("U2: hi")
    print("B : " + str(model.parse(userid_2, "hi")))

    print("U2: yes")
    print("B : " + str(model.parse(userid_2, "yes")))

    print("U2: hi")
    print("B : " + str(model.parse(userid_2, "hi")))

    print("U2: hi")
    print("B : " + str(model.parse(userid_2, "hi")))

    print("U2: hi")
    print("B : " + str(model.parse(userid_2, "hi")))

    print("U2: hi")
    print("B : " + str(model.parse(userid_2, "hi")))

    print("U2: bye")
    print("B : " + str(model.parse(userid_2, "bye")))

    print("********** USER SWITCH **********")

    print("U1: yes")
    print("B : " + str(model.parse(userid_1, "yes")))

    print("U1: bye")
    print("B : " + str(model.parse(userid_1, "bye")))
