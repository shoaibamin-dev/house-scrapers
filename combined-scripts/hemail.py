import os
import smtplib
import imghdr
from email.message import EmailMessage

def send(body, body_template):

    EMAIL_ADDRESS = 'kokokkoa12@gmail.com'
    EMAIL_PASSWORD = 'kaka1111@'


    msg = EmailMessage()
    msg['Subject'] = 'From House Scrapers!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'kokokkoa12@gmail.com'

    msg.set_content(body)

    msg.add_alternative(body_template, subtype='html')


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)