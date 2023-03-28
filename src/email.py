
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(subject, message_body):
    if os.environ.get('SENDGRID_API_KEY') is None:
        raise Exception("SENDGRID_API_KEY is not set")

    from_email = os.environ.get('SENDGRID_FROM_EMAIL')
    to_email = os.environ.get('SENDGRID_TO_EMAIL')

    # print from_email
    print(to_email)
    print(from_email)
    print(subject)

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=message_body)
    try:
        print(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)