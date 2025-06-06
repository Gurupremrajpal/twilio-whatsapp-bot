from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Needed for session management

@app.route('/webhook', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    user_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    if 'step' not in session:
        session['step'] = 'greet'

    # Step 1: Greeting
    if session['step'] == 'greet' and incoming_msg == 'hi':
        msg.body("""
👋 Welcome to HR Dost!
Please choose an option:

Type 1 – Apply for Visiting Card
""")
        session['step'] = 'menu'
        return str(resp)

    # Step 2: User chose visiting card
    elif session['step'] == 'menu' and incoming_msg == '1':
        msg.body("Enter your full name (e.g., Rajnikant Tiwari)")
        session['step'] = 'get_name'
        return str(resp)

    # Step 3: Get name
    elif session['step'] == 'get_name':
        session['name'] = request.values.get('Body', '').strip()
        msg.body("Enter your Employee Number (e.g., BB1234)")
        session['step'] = 'get_emp'
        return str(resp)

    # Step 4: Get emp no and show final options
    elif session['step'] == 'get_emp':
        session['emp'] = request.values.get('Body', '').strip()
        name = session['name']
        emp = session['emp']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Log to Excel Online (placeholder - implement later)
        print(f"Excel Log --> Name: {name}, Emp: {emp}, Time: {timestamp}, Option: Pending")

        msg.body("""
✅ Your visiting card request is ready.

🎯 Final Step — Choose how to send your request:

Option A – Outlook Web (opens browser)
Option B – Copy-paste email text for Outlook app
Option C – Open default email app (Outlook must be default)

Please reply with A, B, or C to continue.
""")
        session['step'] = 'final_choice'
        return str(resp)

    # Step 5: Handle A
    elif session['step'] == 'final_choice' and incoming_msg == 'a':
        msg.body("""
🔗 You must be logged into Outlook Web in your browser to proceed.
If you're logged in, click the link below:

https://outlook.office.com/mail/deeplink/compose?to=hnihr@bajajbroking.in&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in&subject=Request%20for%20Visiting%20Card&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20%0AEmployee%20Number:%20
""")
        return str(resp)

    # Step 6: Handle B
    elif session['step'] == 'final_choice' and incoming_msg == 'b':
        msg.body("""
Copy and paste the following email in Outlook:

To: hnihr@bajajbroking.in
CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in
Subject: Request for Visiting Card

I would like to apply for visiting card.  
Name:  
Employee Number:
""")
        return str(resp)

    # Step 7: Handle C (confirmation step)
    elif session['step'] == 'final_choice' and incoming_msg == 'c':
        msg.body("""
⚠️ Please make sure Outlook is your default email app.
If not, please use Option A or B.

Reply YES to continue with Option C.
""")
        session['step'] = 'confirm_c'
        return str(resp)

    # Step 8: After YES confirmation for C
    elif session['step'] == 'confirm_c' and incoming_msg == 'yes':
        name = session.get('name', '')
        emp = session.get('emp', '')
        mailto_link = (
            "mailto:hnihr@bajajbroking.in"
            "?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
            "&subject=Request%20for%20Visiting%20Card"
            f"&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20{name}%0AEmployee%20Number:%20{emp}"
        )
        msg.body(
            f"📧 Tap the link below to open your email app:\n\n"
            f"[Click to Email](<{mailto_link}>)\n\n"
            f"💡 If nothing happens, Outlook may not be your default app. Try Option A or B instead."
        )
        return str(resp)

    else:
        msg.body("Sorry, I didn't understand. Please type 'Hi' to begin.")
        session['step'] = 'greet'
        return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
