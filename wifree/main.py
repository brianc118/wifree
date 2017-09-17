#!/usr/bin/env python3

import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import datetime
import maps
import traceback

app = Flask(__name__)

# Twilio
account_sid = "TWILIO__SID"
auth_token = "TILIO_TOKEN"
client = Client(account_sid, auth_token)

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
    mode = arr[0]
    if mode != 'walking' and mode != 'driving' and mode != 'transit':
        raise ValueError
    return (mode, str(lat) + ',' + str(lon))

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    print('received message')
    body = request.values.get('Body', None)
    coord = (None, None)
    resp = MessagingResponse()
    try:
        mode, coord = parse_body(body)
    except:
        resp.message('Invalid data')
        return str(resp)

    wifiloc = None
    try:
        message = client.api.account.messages.create(to=request.values.get('From', None),
                                                     from_="+14158531662",
                                                     body='Received message, looking for directions...')
        wifiloc = maps.get_wificoord(coord, mode)
        print(wifiloc)
        directions, travel_time = maps.direction_coordinates(coord, wifiloc[1], mode)
    except:
        traceback.print_exc()
        resp.message('Could not obtain directions')
        return str(resp)
    msg = ''
    msg += wifiloc[0] + "\n"
    msg += 'Time to destination: ' + str(datetime.timedelta(seconds=travel_time))
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
