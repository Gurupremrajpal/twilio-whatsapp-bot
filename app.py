
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import os

app = Flask(__name__)

# In-memory user state tracking (dictionary)
user_state = {}

@app.route('/webhook', methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip()
    user_number = request.values.get('From', '')

    resp = MessagingResponse()
    msg = resp.message()

    # Get current user session or initialize
    state = user_state.get(user_number, {'step': 'greet'})

    step = state['step']

    if step == 'greet' and incoming_msg.lower() == 'hi':
        msg.body("👋 Welcome to HR Dost!\nPlease choose an option:\n\nType 1 – Apply for Visiting Card")
        state['step'] = 'menu'

    elif step == 'menu' and incoming_msg == '1':
        msg.body("Enter your full name (e.g., Rajnikant Tiwari)")
        state['step'] = 'get_name'

    elif step == 'get_name':
        state['name'] = incoming_msg.strip()
        msg.body("Enter your Employee Number (e.g., BB1234)")
        state['step'] = 'get_emp'

    elif step == 'get_emp':
        state['emp'] = incoming_msg.strip()
        name = state['name']
        emp = state['emp']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        state['timestamp'] = timestamp

        msg.body("✅ Your visiting card request is ready.\n\n🎯 Final Step — Choose how to send your request:\n\n"
                 "Option A – Outlook Web (opens browser)\n"
                 "Option B – Copy-paste email text for Outlook app\n"
                 "Option C – Open default email app (Outlook must be default)\n\n"
                 "Please reply with A, B, or C to continue.")
        state['step'] = 'final_choice'

    elif step == 'final_choice' and incoming_msg.lower() == 'a':
        outlook_link = (
            "https://outlook.office.com/mail/deeplink/compose"
            "?to=hnihr@bajajbroking.in"
            "&cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
            "&subject=Request%20for%20Visiting%20Card"
            "&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20%0AEmployee%20Number:%20"
        )
        msg.body(f"🧠 You must be logged into Outlook Web in your browser.\n"
                 f"If you're logged in, tap below:\n\n{outlook_link}")

    elif step == 'final_choice' and incoming_msg.lower() == 'b':
        msg.body("Copy and paste the following email in Outlook:\n\n"
                 "To: hnihr@bajajbroking.in\n"
                 "CC: employeesupport@bajajbroking.in, rajnikant.tiwari@bajajbroking.in, jahnavi.sharma@bajajbroking.in\n"
                 "Subject: Request for Visiting Card\n\n"
                 "I would like to apply for visiting card.\nName: \nEmployee Number:")

    elif step == 'final_choice' and incoming_msg.lower() == 'c':
        msg.body("⚠️ Please make sure Outlook is your default email app.\n"
                 "If not, please use Option A or B.\n\nReply YES to continue with Option C.")
        state['step'] = 'confirm_c'

    elif step == 'confirm_c' and incoming_msg.lower() == 'yes':
        name = state.get('name', '')
        emp = state.get('emp', '')
        mailto_link = (
            "mailto:hnihr@bajajbroking.in"
            "?cc=employeesupport@bajajbroking.in,rajnikant.tiwari@bajajbroking.in,jahnavi.sharma@bajajbroking.in"
            "&subject=Request%20for%20Visiting%20Card"
            f"&body=I%20would%20like%20to%20apply%20for%20visiting%20card.%0AName:%20{name}%0AEmployee%20Number:%20{emp}"
        )
        msg.body(f"📧 Tap below:\n{mailto_link}\n\n(Works only if Outlook is default email app)")

    else:
        msg.body("Sorry, I didn't understand. Please type 'Hi' to begin.")
        state['step'] = 'greet'

    # Save state back
    user_state[user_number] = state
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
