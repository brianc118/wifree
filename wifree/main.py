import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    # incomingnumber = request.values.get('From', None)
    print('received message')
    body = request.values.get('Body', None)

    resp = MessagingResponse()
    resp.message(body)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
