import smtplib
from email.mime.text import MIMEText

# Email details
sender = "jdomingoplaza@gmail.com"
receiver = "jdplaza@miuandes.cl"
subject = "Testing liciagent email"
body = "This is the first step of many!"

# Create message
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

# Send email (using Gmail's SMTP server as example)
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, "niaq hgcv lxft wpnm")  # Use an app password, not your main password
    server.sendmail(sender, receiver, msg.as_string())