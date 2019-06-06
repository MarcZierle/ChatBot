class QuerentParser():

    def __init__(self, json):
        self.__json = json
        self.__destinations = json['destination_addresses']
        self.__origins = json['origin_addresses']

        self.__durations = []
        for elem in json['rows']:
            for dur in elem['elements']:
                self.__durations.append(round(dur['duration']['value']/60))

        self.__distances = []
        for elem in json['rows']:
            for dist in elem['elements']:
                self.__distances.append(round(dist['distance']['value']))


    # in minutes
    def get_durations(self):
        return self.__durations


    # in meters
    def get_distances(self):
        return self.__distances


    def get_destinations(self):
        return self.__destinations


    def get_origins(self):
        return self.__origins


    def __str__(self):
        return str(self.__json)
