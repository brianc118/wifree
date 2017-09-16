import googlemaps
from datetime import datetime
import json
from bs4 import BeautifulSoup
gmaps = googlemaps.Client(key='GMAPS_KEY')


# Request directions via public transit
def direction_co_ordinates(user_location, direction_location):

    now = datetime.now()
    directions_result = gmaps.directions(user_location,
                                     direction_location,
                                     mode="driving",
                                     departure_time=now)
    steps = directions_result[0]['legs'][0]['steps']
    for step in steps:
        print  BeautifulSoup(step['html_instructions']).get_text()
#print(json.dumps(directions_result[0], indent=2))

user_location = '-33.873157,151.206116'
direction_location = '-33.815000,151.001111'
direction_co_ordinates(user_location,direction_location)