const express = require('express');
const { MessagingResponse } = require('twilio').twiml;

const app = express();
app.use(express.urlencoded({ extended: false }));

const sessions = {};

app.post('/webhook', (req, res) => {
  const twiml = new MessagingResponse();
  const msg = req.body.Body.trim().toLowerCase();
  const from = req.body.From;

  if (!sessions[from]) sessions[from] = { step: 0 };

  const user = sessions[from];

  if (msg === 'hi' || user.step === 0) {
    twiml.message(`👋 Welcome to HR Dost!
Please choose an option:

Apply for Visiting Card

Type 1 to continue`);
    user.step = 1;
  } else if (msg === '1' && user.step === 1) {
    twiml.message(`Enter your full name (e.g., Rajnikant Tiwari)`);
    user.step = 2;
  } else if (user.step === 2) {
    user.name = req.body.Body.trim();
    twiml.message(`Enter your employee number (e.g., BB1234)`);
    user.step = 3;
  } else if (user.step === 3) {
    user.empId = req.body.Body.trim();
    twiml.message(`🎯 Final Step — Choose how to send your request:

A – Outlook Web
B – Copy Email Text
C – Default Email App

Reply with A, B, or C`);
    user.step = 4;
  } else if (user.step === 4) {
    const option = msg.toUpperCase();
    const { name, empId } = user;

    const timestamp = new Date().toISOString();

    if (option === 'A') {
      const mailLink = `https://outlook.office.com/mail/deeplink/compose?subject=Visiting%20Card%20Request&body=Name:%20${encodeURIComponent(name)}%0AEmployee%20ID:%20${encodeURIComponent(empId)}`;
      twiml.message(`📤 Click below to send email via Outlook Web:
${mailLink}`);
    } else if (option === 'B') {
      twiml.message(`✉️ Copy & paste this in your Outlook app:

Subject: Visiting Card Request

Name: ${name}
Employee ID: ${empId}`);
    } else if (option === 'C') {
      const mailto = `mailto:hr@example.com?subject=Visiting%20Card%20Request&body=Name:%20${encodeURIComponent(name)}%0AEmployee%20ID:%20${encodeURIComponent(empId)}`;
      twiml.message(`📧 Tap below:
${mailto}

(Works only if Outlook is default email app)`);
    } else {
      twiml.message(`Invalid option. Please reply with A, B, or C.`);
    }

    console.log({ name, empId, option: msg.toUpperCase(), timestamp });
    user.step = 0;
  } else {
    twiml.message(`Type "Hi" to restart.`);
    user.step = 0;
  }

  res.type('text/xml');
  res.send(twiml.toString());
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Bot running on port ${PORT}`));
