import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings

def send_email(sender, receiver, subject, message_text, message_html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{}'.format(subject)
    msg['From'] = '{}'.format(sender)
    msg['To'] = '{}'.format(receiver)
    text = message_text
    html = message_html
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(settings.EMAIL_HOST_USER[0], settings.EMAIL_HOST_PASSWORD[0])
    try:
        smtpObj.sendmail(sender, receiver, msg.as_string())
        smtpObj.quit()
        print("Successfully sent email")
    except SMTPException:
        print("Error: unable to send email")
