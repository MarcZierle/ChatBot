import datetime as dt

import googledistancematrix as gdm
from googledistancematrix import querent

import settings
settings.init()

gdm_querent = gdm.querent.Querent( api_key=settings.GOOGLE_DISTANCE_MATRIX_API_KEY )
gdm_querent.settravelmode(gdm.querent.Querent.TravelMode.TRANSIT)

details = gdm_querent.gettraveldetails(
    origins = ["Rudower Straße 25 Berlin"],
    destinations = ["Str. d. Pariser Kommune 30 Berlin"],
    arrival_time = dt.datetime(2019, 5, 23, 22, 7)
)

print(details['rows'][0]['elements'][0]['duration']['value'])
