import os
from email.policy import SMTPUTF8
from mailbox import Message
from smtplib import SMTP, SMTP_SSL
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

def send_mail(receiver_address: str, subject: str, body: str, sender_address: str = "admin@vcp-medingen.de"):
    message = Message()
    message.set_payload(body, charset="utf-8")
    message["Subject"] = subject

    smtp.send_message(message, sender_address, receiver_address, mail_options=["SMTPUTF8"])

def close():
    smtp.quit()