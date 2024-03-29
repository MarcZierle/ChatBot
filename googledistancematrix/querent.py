import urllib.parse as up
import urllib.request as ur, json
import datetime
from datetime import timezone
from enum import Enum

class Querent():
    """
    Used to prepare the local part for an HTTP(S) connection to use the Google Distance Matrix API service.
    Returned objects will always be in JSON format only. Units will always be metric.
    Transit modes will be via public transportation and/or walking.

    And yes, according to
    `Google Ngram <https://books.google.com/ngrams/graph?content=queryer%2Cquerier%2Cquerist%2C(querant%2Bquerent)&year_start=1960&year_end=2000&corpus=15&smoothing=3&share=&direct_url=t1%3B%2Cquerier%3B%2Cc0%3B.t1%3B%2Cquerist%3B%2Cc0%3B.t1%3B%2C%28querant%20%2B%20querent%29%3B%2Cc0>`_
    the proper naming for somone who is querying for something may be called a querent (querant). :D
    """

    # base query URL
    base_url = ("https://maps.googleapis.com/maps/api/distancematrix"
                "/json?"
                "units=metric"
                "&language=en"
                "&region=de")


    global TravelMode
    class TravelMode(Enum):
        TRANSIT = "transit"
        WALKING = "walking"
        DRIVING = "driving"
        BICYCLING = "bicycling"


    __api_count = 0


    def __init__(self, api_key):
        """
        Initilize the Querent and provide the API key for later usageself.

        Parameters
        ----------
        api_key : string
            The API key used for querying the Google Distance Matrix API service.
        """
        self.__api_key = api_key
        self.set_travel_mode(TravelMode.TRANSIT)


    def get_api_count(self):
        return Querent.__api_count


    def get_travel_details(self, origins, destinations, departure_time='', arrival_time=''):
        """
        Receive all travel details in respect to a specific traveling route
        given by it's origin, destination and time of departure / arrival.

        Parameters
        ----------
            origin : string
                The location where to route will be started.
            destination : string
                The location where to route will be ended.
            departure_time : datetime
                Optional: The date and time since when the route begins.
                GMT is expected and will be converted to GMT+2.
                Mutually exclusive to arrival_time.
            arrival_time : datetime
                Optional: The date and time the route will end.
                GMT is expected and will be converted to GMT+2.
                Mutually exclusive to departure_time.

        Returns
        -------
            JSON-object
                The response from the Google Distance Matrix API service.
        """

        # check that departure_time and arrival_time are not set at the same time
        if not departure_time and not arrival_time:
            time = "&departure_time=now"
        elif not departure_time and arrival_time:
            time = "&arrival_time=" + str(Querent.__datetime_to_seconds(arrival_time));
        elif departure_time and not arrival_time:
            time = "&departure_time=" + str(Querent.__datetime_to_seconds(departure_time));
        else:
            raise Exception ("departure_time and arrival_time may only be used mutually exclusive or omitted at all.")

        # build the query url
        query_url = (Querent.base_url +
            "&key=" +
                self.__api_key +
            "&origins=" +
                Querent.__list_to_string(origins) +
            "&destinations=" +
                Querent.__list_to_string(destinations) +
            "&mode=" +
                self.__travel_mode +
            time)

        return self.__send_url_request(query_url)


    def get_place_address(self, place):
        query_url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/"
            + "json?"
            + "key=" + str(self.__api_key)
            + "&inputtype=textquery"
            + "&language=en"
            + "&fields=formatted_address"
            + "&input=" + str(place)
            )

        response = self.__send_url_request(query_url)

        if response['status'] == "OK":
            return response['candidates'][0]['formatted_address']
        else:
            return None


    def set_travel_mode(self, mode):
        self.__travel_mode = mode.value


    def __send_url_request(self, url_str):
        """
        Sends a HTTP(S) request to the specified URL and returns a JSON object of the response.

        Parameters
        ----------
            url_str : string
                The URL used for the request.

        Returns
        -------
            JSON-object
                A JSON-object / dictionary of the response.
        """
        # escape any character that needs to be
        url_str = up.quote(url_str, safe='/:?&=.,+-_%|') # characters to be preserved when escaping the url
        response = ur.urlopen(url_str)
        Querent.__api_count = Querent.__api_count + 1
        #print(url_str)
        return json.loads(response.read())


    def __list_to_string(lst):
        """
        Converts a list of strings to a single string divided by the pipe operator ('|').

        Parameters
        ----------
            lst : list / string
                The list or string to be converted.

        Returns
        -------
            string
                A single string containing each list element concatenated.
        """
        if isinstance(lst, (list,)):    # check list type
            return '|'.join(lst)
        elif isinstance(lst, str):      # check string type
            return lst
        else:
            raise Exception ("Type may be list or string only.")


    def __datetime_to_seconds(date):
        """
        Returns the time difference in seconds between date and midnight, January 1, 1970 UTC.

        Parameters
        ----------
            date : datetime
                The date to be converted.
                GMT is expected and will be converted to GMT+2 at first and eventually to UTC.

        Returns
        -------
            int
                The time difference in seconds.
        """
        date = date - datetime.timedelta(hours=2);  # removes two hours of timezone and summer time
        return int(date.replace(tzinfo=timezone.utc).timestamp()) # convert to UTC seconds since 1970/01/01
        #epoch = datetime.datetime.utcfromtimestamp(0)
        #return int((date - epoch).total_seconds())
