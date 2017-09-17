#!/usr/bin/env python3

import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import maps
import traceback

app = Flask(__name__)

def parse_body(body):
    arr = body.split(',')
    if len(arr) != 2:
        raise ValueError
    lat = float(arr[0])
    lon = float(arr[1])
    if lat < -90 or lat > 90:
        raise ValueError
    if lon < -180 or lon > 180:
        raise ValueError
    return str(lat) + ',' + str(lon)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    print('received message')
    body = request.values.get('Body', None)
    coord = (None, None)
    resp = MessagingResponse()
    try:
        coord = parse_body(body)
    except:
        resp.message('Invalid data')
        return str(resp)

    wifiloc = None
    try:
        wifiloc = maps.get_wificoord(coord, 'walking')
        print(wifiloc)
        directions = maps.direction_coordinates(coord, wifiloc[1], 'walking')
    except:
        traceback.print_exc()
        resp.message('Could not obtain directions')
        return str(resp)
    msg = ''
    msg += wifiloc[0]
    for step in directions:
        msg += ('\n' + step)
    resp.message(msg)
    return str(resp)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
