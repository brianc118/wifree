import googlemaps
import datetime
import json
from bs4 import BeautifulSoup
import foursquare
import math

gmaps = googlemaps.Client(key='GMAPS_KEY')


# Request directions via public transit
def direction_coordinates(user_location, direction_location, mode):
    now = datetime.datetime.now()
    directions_result = gmaps.directions(user_location,
                                     direction_location,
                                     mode=mode,
                                     departure_time=now)
    total_time = get_time(user_location, direction_location, mode)
    steps = directions_result[0]['legs'][0]['steps']
    arr = []
    for step in steps:
        arr.append(BeautifulSoup(step['html_instructions'].replace('<div', '\n<div'), 'lxml').get_text())
    return (arr, total_time)

def get_time(user_location, direction_location, mode):
    now = datetime.datetime.now()
    directions_result = gmaps.directions(user_location,
                                     direction_location,
                                     mode=mode,
                                     departure_time=now)
    # print("Directions_result = " + str(directions_result))
    if len(directions_result) == 0:
        return 9999999999999999999
    return sum([sum([step['duration']['value'] for step in leg['steps']]) for leg in directions_result[0]['legs']])


client = foursquare.Foursquare(client_id='4SQ_ID', client_secret='4SQ_SECRET')

max_travel_time = 120 # in min
rad_min = 2000
rad_max = 16000

def get_coord(result):
    name = result[u'name']
    loc = result[u'location']
    lat = loc[u'lat']
    lng = loc[u'lng']
    return (name, str(lat) + ',' + str(lng))

def get_wificoord(location, mode):
    results = []
    # for i in range (math.floor(math.log(rad_min,rad_max))):
        # try:
    radius = 16000
    rawresults = client.venues.explore(params={'query': 'Wifi', 'll': location, 'limit': 50})
    results = []
    for rawresultsgroup in rawresults[u'groups']:
        results += [(item['venue'], get_time(location, get_coord(item['venue'])[1], mode)) for item in rawresultsgroup[u'items']]

    rawresults = client.venues.explore(params={'query': 'Free Wifi', 'll': location, 'limit': 50})
    for rawresultsgroup in rawresults[u'groups']:
        results += [(item['venue'], get_time(location, get_coord(item['venue'])[1], mode)) for item in rawresultsgroup[u'items']]
    results.sort(key=lambda x:x[1], reverse=False)
    for r, t in results:
        print(r['name'] + '\t' + str(t))
    return get_coord(results[0][0])  # return shortest
        # except:
            # pass
    # raise Exception
    # return ''
    

