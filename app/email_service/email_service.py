import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

from ..config import Config


def send_email()

sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
from_email = Email("aavishkargautam@gmail.com")
to_email = To("ag8298@nyu.edu")  # Change to your recipient
subject = "Checking twilio's email"
content = Content("text/plain", "Hey. Just a email to check if the thing is working fine.")
mail = Mail(from_email, to_email, subject, content)

# Get a JSON-ready representation of the Mail object
mail_json = mail.get()


# Send an HTTP POST request to /mail/send
response = sg.client.mail.send.post(request_body=mail_json)
print(response.status_code)
print(response.headers)

