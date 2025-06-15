import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import pprint

from ..config import Config


def send_reminder_email(
    receipient_email,
    subject,
    content
):
    sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
    from_email = Email(Config.sender_email)
    to_email = To(receipient_email)
    content = Content("text/plain", content)

    mail = Mail(from_email, to_email, subject, content)

    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body = mail_json)

    return response.status_code


def send_dynamic_email(
    receipient_email,
    subject,
    dynamic_template,
    template_id
):

    sg = sendgrid.SendGridAPIClient(api_key=Config.SENDGRID_API_KEY)
    from_email = Email(Config.sender_email)
    to_email = To(receipient_email)  # Change to your recipient

    mail = Mail(from_email, to_email, subject)

    # Add template_id and dynamic_template
    mail.template_id = template_id
    mail.dynamic_template_data = dynamic_template

    # pprint.pp(mail)

    # # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)


if "__main__" == __name__:
    dynamic_template = {
        "receipient_name":"Aavishkar",
        "portal_url":"https://students.nyuad.nyu.edu/",
        "date": "June 14, 2025",
        "summary": "Today's announcements include a new AI Ethics course, a planned website downtime, and an update to the faculty portal for faster login."    
    }
    template_id = "d-160958b06b8d4812b18dbaf621882b2a"

    send_dynamic_email(
        "ag8298@nyu.edu",
        "Testing the first PortalPeek Update",
        dynamic_template,
        template_id
    )