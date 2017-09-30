#!/usr/bin/env python3

import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime
import maps
import traceback

from keys import TWILIO_SID, TWILIO_TOKEN

app = Flask(__name__)

client = Client(TWILIO_SID, TWILIO_TOKEN)

printReceivedMessage = False

def parse_body(body):
    arr = body.split(',')
    if len(arr) != 3:
        raise ValueError
    lat = float(arr[1])
    lon = float(arr[2])
    if lat < -90 or lat > 90:
        raise ValueError
    if lon < -180 or lon > 180:
        raise ValueError
    mode = arr[0].lower()
    if mode != 'walking' and mode != 'driving' and mode != 'transit':
        raise ValueError
    return (mode, str(lat) + ',' + str(lon))

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    print('received message')
    body = request.values.get('Body', None)
    coord = ''
    resp = MessagingResponse()
    try:
        mode, coord = parse_body(body)
    except:
        resp.message('Invalid request. Must be in form [travelmode],[latitude],[longitude]. For example: walking,42.3585,-71.0964')
        return str(resp)

    wifiloc = None
    try:
        if printReceivedMessage:
            message = client.api.account.messages.create(to=request.values.get('From', None),
                                                         from_="+14158531662",
                                                         body='Received message, looking for directions...')
        wifiloc = maps.get_bestcoord(coord, mode)
        print(wifiloc)
        directions, travel_time, travel_dist = maps.direction_coordinates(coord, wifiloc[1], mode)
    except:
        traceback.print_exc()
        resp.message('Could not obtain directions')
        return str(resp)
    msg = wifiloc[0] + '\n'
    msg += 'Time to destination: ' + str(datetime.timedelta(seconds=travel_time))
    msg += '(' + str(travel_dist/1000) + 'km / ' + str(travel_dist/1000*0.621371) + 'miles )\n'
    for step in directions:
        msg += ('\n' + step)
    try:
        message = client.api.account.messages.create(to=request.values.get('From', None),
                                                     from_="+14158531662",
                                                     body=msg)
    except:
        print('Error: couldn\'t send message')
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
