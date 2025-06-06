from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == 'hi':
        msg.body("👋 Welcome to HR Dost!\nPlease choose an option:\n\nType 1 – Apply for Visiting Card")
    elif incoming_msg == '1':
        msg.body("Enter your full name (e.g., Rajnikant Tiwari)")
    elif incoming_msg.startswith('name:'):
        msg.body("Enter your employee number (e.g., BB1234)")
    elif incoming_msg.startswith('emp:'):
        msg.body("✅ Your visiting card request is ready.\n\n🎯 Final Step — Choose how to send your request:\nOption A – Outlook Web (opens auto-filled email in browser)\nOption B – Copy-paste email text into your Outlook app\nOption C – Open default email app (Outlook must be default)\n\nPlease reply with A, B, or C to continue.")
    elif incoming_msg == 'a':
        msg.body("ℹ️ Please ensure you're logged into Outlook Web.\nThen click below and fill in your name and employee number manually:\n\nhttps://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName%3A%20%0AEmployee%20Number%3A")
    elif incoming_msg == 'b':
        msg.body("✉️ Copy and paste the following email into your Outlook app:\n\nTo: hnihr@bajajbroking.in\nCC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in\nSubject: Request for Visiting Card\n\nI would like to apply for visiting card.\nName:\nEmployee Number:")
    elif incoming_msg == 'c':
        msg.body("⚠️ Make sure Outlook is your default email app.\nIf not, please use Option A or B.\n\nmailto:hnihr@bajajbroking.in?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%0AEmployee%20Number:")
    else:
        msg.body("Invalid option. Please type 'Hi' to restart.")

    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
