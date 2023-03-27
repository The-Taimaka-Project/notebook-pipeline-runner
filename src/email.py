# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

standard_error_message = """
There was an error. Please check the pipeline and
associated error logs for more information.
"""


def send_error_email(append_message):
    send_email(standard_error_message + append_message,
               "Pipeline Error",


def send_email(message, subject, recipient, sender):
    msg = EmailMessage()
    msg.set_content(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
