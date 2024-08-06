import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import os

def send_email(sender_email, sender_password, receiver_email, subject, body, attachments):
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Add attachments
    for attachment in attachments:
        filename = os.path.basename(attachment)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(attachment, "rb") as f:
                img = MIMEImage(f.read(), name=filename)
                message.attach(img)
        else:
            with open(attachment, "rb") as f:
                part = MIMEApplication(f.read(), Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                message.attach(part)

    # Create SMTP session
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

# Usage
sender_email = f"{os.environ.get('EMAIL_SENDER')}@gmail.com"
sender_password = os.environ.get('EMAIL_APP_PASS')
receiver_email = f"{os.environ.get('EMAIL_RECEIVER')}@gmail.com"
subject = "Latest Rotterdam Appointment Times"
date_time = open('date_time.txt', 'r', encoding="utf-8").read()
body = f"Next appointment {date_time}"

attachments = ["calendar.png", "options.png"]

send_email(sender_email, sender_password, receiver_email, subject, body, attachments)