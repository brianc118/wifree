import googlemaps
import datetime
import json
from bs4 import BeautifulSoup
import foursquare
import math

from keys import FOURSQUARE_ID, FOURSQUARE_SECRET, GMAPS_KEY

wifiSearchTerms = ['Wifi', 'Free Wifi']

client = foursquare.Foursquare(client_id=FOURSQUARE_ID, client_secret=FOURSQUARE_SECRET)

def get_coord(result):
    name = result[u'name']
    loc = result[u'location']
    lat = loc[u'lat']
    lng = loc[u'lng']
    return (name, str(lat) + ',' + str(lng))

def get_wificoord(location):
    results = []

    for term in wifiSearchTerms:
        rawresults = client.venues.explore(params={'query': 'Wifi', 'll': location, 'limit': 50})
        for rawresultsgroup in rawresults[u'groups']:
            results += [get_coord(item['venue'])[1] for item in rawresultsgroup['items']]

    return results
    

gmaps = googlemaps.Client(key=GMAPS_KEY)

user_location = (30.2927, -97.7447)  # Rio
destinations = get_wificoord('30.2927, -97.7447')

res = gmaps.distance_matrix([user_location], destinations, mode='driving')

min(res['rows'][0]['elements'], key=lambda x : x['duration']['value'])






