from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    print("📩 Received message:", incoming_msg)

    if incoming_msg == 'hi':
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>👋 Welcome to HR Dost!
Please choose an option:

Type 1 – Apply for Visiting Card</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg == '1':
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Enter your full name (e.g., Rajnikant Tiwari)</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg.startswith('name:'):
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Enter your employee number (e.g., BB1234)</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg.startswith('emp:'):
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>✅ Your visiting card request is ready.

🎯 Final Step — Choose how to send your request:
A – Outlook Web
B – Copy-paste text
C – Default Email App

Reply with A, B, or C to continue.</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg == 'a':
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>ℹ️ Please log in to Outlook Web.

Click below and fill manually:
https://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%0AEmployee%20Number:</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg == 'b':
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>✉️ Copy this email and paste into your Outlook App:

To: hnihr@bajajbroking.in  
CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in  
Subject: Request for Visiting Card

I would like to apply for visiting card.  
Name:  
Employee Number:</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    elif incoming_msg == 'c':
        reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>⚠️ Make sure Outlook is your default app.

If not, please use Option A or B.

mailto:hnihr@bajajbroking.in?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%0AEmployee%20Number:</Message>
</Response>"""
        return Response(reply, mimetype='application/xml')

    # Default fallback
    reply = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>❌ Invalid input. Please type "Hi" to restart the flow.</Message>
</Response>"""
    return Response(reply, mimetype='application/xml')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 HR Dost Bot running on port {port}")
    app.run(host='0.0.0.0', port=port)
