# Twilio WhatsApp Bot – HR Dost

This is a simple Node.js backend for WhatsApp bot using Twilio Sandbox.

## Features

- WhatsApp bot flow using Twilio Messaging Webhooks
- Collects name and employee ID
- Gives 3 email options to send request
- Console logs the responses (can be connected to Excel)

## To Run Locally

```bash
npm install
npm start
```

## Deploy to Render

1. Push to GitHub
2. Go to [Render.com](https://render.com)
3. Create new Web Service → Connect GitHub
4. Use `/webhook` as endpoint
5. Paste the Render URL into Twilio Sandbox webhook field
