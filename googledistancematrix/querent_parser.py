class QuerentParser():

    def __init__(self, json):
        self.__json = json
        self.__destinations = json['destination_addresses']
        self.__origins = json['origin_addresses']

        self.__durations = []
        for elem in json['rows']:
            self.__durations.append(round(elem['elements'][0]['duration']['value']/60))

        self.__distances = []
        for elem in json['rows']:
            self.__distances.append(round(elem['elements'][0]['distance']['value']))


    # in minutes
    def get_duations(self):
        return self.__durations


    # in meters
    def get_distances(self):
        return self.__distances


    def __str__(self):
        return str(self.__json)
