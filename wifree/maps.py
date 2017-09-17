import googlemaps
from datetime import datetime
import json
from bs4 import BeautifulSoup
gmaps = googlemaps.Client(key='GMAPS_KEY')


# Request directions via public transit
def direction_coordinates(user_location, direction_location, mode):
    now = datetime.now()
    directions_result = gmaps.directions(user_location,
                                     direction_location,
                                     mode=mode,
                                     departure_time=now)
    steps = directions_result[0]['legs'][0]['steps']
    arr = []
    for step in steps:
        arr.append(BeautifulSoup(step['html_instructions'], 'lxml').get_text())
    return arr
