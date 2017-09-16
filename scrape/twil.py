from twilio.rest import Client

def twilmsg(messagestr, numberstr):
	account_sid = "TWILIO__SID"
	auth_token = "TILIO_TOKEN"

	client = Client(account_sid, auth_token)

	message = client.messages.create(
	    to=numberstr, 
	    from_="+14158531662",
	    body=messagestr)