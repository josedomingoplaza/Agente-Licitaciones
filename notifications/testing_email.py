import os
import smtplib
from email.mime.text import MIMEText
import dotenv
dotenv.load_dotenv()

password = os.getenv("EMAIL_PASSWORD")

sender = "jdomingoplaza@gmail.com"
receiver = "jdplaza@miuandes.cl"
subject = "Testing liciagent email"
body = "This is the first step of many!"

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password) 
    server.sendmail(sender, receiver, msg.as_string())

print("Email sent successfully!")