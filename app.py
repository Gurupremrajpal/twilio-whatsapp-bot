from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()

    if incoming_msg == 'hi':
        return Response('''<Response><Message>👋 Welcome to HR Dost!
Please choose an option:\n\nType 1 – Apply for Visiting Card</Message></Response>''', mimetype='application/xml')

    elif incoming_msg == '1':
        return Response('''<Response><Message>Enter your full name (e.g., Rajnikant Tiwari)</Message></Response>''', mimetype='application/xml')

    elif incoming_msg.startswith('name:'):
        return Response('''<Response><Message>Enter your employee number (e.g., BB1234)</Message></Response>''', mimetype='application/xml')

    elif incoming_msg.startswith('emp:'):
        return Response('''<Response><Message>✅ Your visiting card request is ready.

🎯 Final Step — Choose how to send your request:
Option A – Outlook Web (opens auto-filled email in browser)
Option B – Copy-paste email text into your Outlook app
Option C – Open default email app (Outlook must be default)

Please reply with A, B, or C to continue.</Message></Response>''', mimetype='application/xml')

    elif incoming_msg == 'a':
        return Response('''<Response><Message>ℹ️ Please ensure you're logged into Outlook Web.
Then click below and fill in your name and employee number manually:

https://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName%3A%20%0AEmployee%20Number%3A</Message></Response>''', mimetype='application/xml')

    elif incoming_msg == 'b':
        return Response('''<Response><Message>✉️ Copy and paste the following email into your Outlook app:

To: hnihr@bajajbroking.in
CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in
Subject: Request for Visiting Card

I would like to apply for visiting card.
Name:
Employee Number:</Message></Response>''', mimetype='application/xml')

    elif incoming_msg == 'c':
        return Response('''<Response><Message>⚠️ Make sure Outlook is your default email app.
If not, please use Option A or B.

mailto:hnihr@bajajbroking.in?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%0AEmployee%20Number:</Message></Response>''', mimetype='application/xml')

    return Response("<Response><Message>Invalid option. Please type 'Hi' to restart.</Message></Response>", mimetype='application/xml')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
