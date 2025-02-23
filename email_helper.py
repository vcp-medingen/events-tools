import os
from email.message import EmailMessage
from smtplib import SMTP

from dotenv import load_dotenv


def init():
    load_dotenv()
    global smtp
    smtp = SMTP(os.environ.get("SMTP_HOST"), os.environ.get("SMTP_PORT"))
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASSWORD"))

def test(mail_address: str):
    smtp.sendmail(os.environ.get("SMTP_USER"), mail_address, "Subject: Test\nThis is a test email. äüö", mail_options=["smtputf8"])

def send_mail(receiver_address: str, subject: str, body: str, sender_address: str = "admin@vcp-medingen.de", html: bool = False):
    message = EmailMessage()
    if html:
        message.set_content(body, subtype="html", charset="utf-8")
    else:
        message.set_payload(body, charset="utf-8")
    message["Subject"] = subject
    message["From"] = sender_address
    message["To"] = receiver_address

    smtp.send_message(message, sender_address, receiver_address, mail_options=["SMTPUTF8"])


def close():
    smtp.quit()