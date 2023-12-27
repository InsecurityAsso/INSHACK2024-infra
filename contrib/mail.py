import os
import pathlib
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

Body = open(path / "New message.html", "r").read()
creds = json.load(open(path / "mail_creds.json", "r"))

def send_mail(dest, subject="Notification", content=Body):
    message = MIMEMultipart()
    dest = message["To"] = dest
    sender = creds.get("mail")
    sender_name = "INS'Hack 2024"
    message["From"] = f"{sender_name} <{sender}>"
    message["Subject"] = f"INS'HACK 2024 | {subject}"

    message.attach(MIMEText(content, "html"))

    server = smtplib.SMTP_SSL("smtppro.zoho.eu", 465)

    server.login(sender, creds.get("password"))

    server.sendmail(sender, dest, message.as_string())

    server.quit()

