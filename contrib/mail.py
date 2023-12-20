import os
import pathlib
import smtplib
import json

# send html or plaintext message
from email.mime.text import MIMEText
# send attachments
from email.mime.multipart import MIMEMultipart

# email and password
message  = MIMEMultipart()

path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

Body = open(path /  "New message.html", "r").read()
creds = json.load(open(path / "mail_creds.json", "r"))

def send_mail(dest, subject="Notification"):
    dest = message["To"] = dest
    sender = creds.get("mail") 
    # set sender to a alphanumerical string instead of an email address
    message["From"] = f"INS'Hack 2024 <{sender}>"
    message["Subject"] = f"INS'HACK 2024 | {subject}"

    message.attach(MIMEText(Body, "html"))

    server = smtplib.SMTP_SSL("smtppro.zoho.eu", 465)

    server.login(sender, creds.get("password")) #"Ins'hack_1s_Fun!"

    server.sendmail(sender, dest, message.as_string())

    server.quit()



