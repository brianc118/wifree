import foursquare

client = foursquare.Foursquare(client_id='4SQ_ID', client_secret='4SQ_SECRET')

def get_wificoord(location):
    # venue search see https://developer.foursquare.com/docs/venues/search
    results = client.venues.explore(params={'query': 'wifi', 'll': location})
    topresult = results[u'groups'][0][u'items'][0][u'venue']
    topresultname = topresult[u'name']
    topresultloc = topresult[u'location']
    topresultlat = topresultloc[u'lat']
    topresultlng = topresultloc[u'lng']

    return (topresultname, str(topresultlat) + ',' + str(topresultlng))