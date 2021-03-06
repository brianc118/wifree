import googlemaps
import datetime
import json
from bs4 import BeautifulSoup
import foursquare
import math

from keys import FOURSQUARE_ID, FOURSQUARE_SECRET, GMAPS_KEY

wifiSearchTerms = ['Wifi', 'Free Wifi']

foursqclient = foursquare.Foursquare(client_id=FOURSQUARE_ID, client_secret=FOURSQUARE_SECRET)
gmapsclient = googlemaps.Client(key=GMAPS_KEY)


def direction_coordinates(user_location, direction_location, mode):
    """ :type user_location: str ('lat,long')
        :type direction_location: str ('lat,long')
        :rtype: tuple (List (directions), Int (total time in s), Float (total distance))
    """
    now = datetime.datetime.now()
    directions_result = gmapsclient.directions(user_location,
                                     direction_location,
                                     mode=mode,
                                     departure_time=now)
    if len(directions_result) == 0:
        return ([], math.inf)
    total_time = sum([sum([step['duration']['value'] for step in leg['steps']]) for leg in directions_result[0]['legs']])
    total_dist = sum([sum([step['distance']['value'] for step in leg['steps']]) for leg in directions_result[0]['legs']])
    steps = directions_result[0]['legs'][0]['steps']
    arr = []
    for step in steps:
        arr.append(BeautifulSoup(step['html_instructions'].replace('<div', '\n<div'), 'lxml').get_text())
    return (arr, total_time, total_dist)

def get_coord(result):
    name = result['name']
    loc = result['location']
    lat = loc['lat']
    lng = loc['lng']
    return (name, str(lat) + ',' + str(lng))

def get_wificoord(location):
    results = []

    for term in wifiSearchTerms:
        rawresults = foursqclient.venues.explore(params={'query': term, 'll': location, 'limit': 50})
        for rawresultsgroup in rawresults['groups']:
            results += [get_coord(item['venue']) for item in rawresultsgroup['items']]
    return results

def get_bestcoord(location, mode):
    dest = get_wificoord(location)
    destnames = [x[0] for x in dest]
    destlatlong = [x[1] for x in dest]
    res = gmapsclient.distance_matrix([location], destlatlong, mode=mode)
    best_i, best_v = min(enumerate(res['rows'][0]['elements']), key=lambda x : x[1]['duration']['value'])
    return (destnames[best_i], destlatlong[best_i], best_v['duration']['value'])