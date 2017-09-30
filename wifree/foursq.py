import foursquare

from keys import FOURSQUARE_ID, FOURSQUARE_SECRET

client = foursquare.Foursquare(client_id=FOURSQUARE_ID, client_secret=FOURSQUARE_SECRET)

def get_wificoord(location):
    # venue search see https://developer.foursquare.com/docs/venues/search
    results = client.venues.explore(params={'query': 'Free Wifi', 'll': location})
    topresult = results[u'groups'][0][u'items'][0][u'venue']
    topresultname = topresult[u'name']
    topresultloc = topresult[u'location']
    topresultlat = topresultloc[u'lat']
    topresultlng = topresultloc[u'lng']

    return (topresultname, str(topresultlat) + ',' + str(topresultlng))
