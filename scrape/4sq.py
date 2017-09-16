import foursquare

client = foursquare.Foursquare(client_id='4SQ_ID', client_secret='4SQ_SECRET')

# venue search see https://developer.foursquare.com/docs/venues/search
geostr = '42.360082,-71.058880'
results = client.venues.explore(params={'query': 'wifi', 'll': geostr})
topresult = results[u'groups'][0][u'items'][0][u'venue']
# results = client.venues.search(params={'query': 'Coffeeshops with WiFi', 'll': geostr, 'intent': 'checkin'})
# topresult = results[u'venues'][0]
topresultname = topresult[u'name']
topresultloc = topresult[u'location']

topresultlat = topresultloc[u'lat']
topresultlng = topresultloc[u'lng']

