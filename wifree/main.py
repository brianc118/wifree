import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

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
    try:
        coord = parse_body(body)
    except:
        return

    resp = MessagingResponse()
    resp.message(body)

    return str(resp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
