import time
from email.mime.text import MIMEText
import smtplib
import subprocess
import sys
import os
import configparser

conf_path = os.path.dirname(__file__)+"/config"
conf = configparser.ConfigParser()
if not conf.read(conf_path):
    raise FileNotFoundError(conf_path)

filename = os.path.basename(__file__)
sender_email = eval(conf.get('MAIL', 'sender_email'))
sender_password = eval(conf.get(filename, 'sender_password'))
receiver_email = eval(conf.get('MAIL', 'receiver_email'))
subject = eval(conf.get(filename, 'subject'))
smtp_server = eval(conf.get('MAIL', 'smtp_server'))
smtp_port = eval(conf.get('MAIL', 'smtp_port'))

try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

previous_status = psutil.sensors_battery().power_plugged

while True:
    current_status = psutil.sensors_battery().power_plugged
    if current_status != previous_status:
        if current_status:
            message = "Device is charging"
        else:
            message = "Device is not charging"

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    previous_status = current_status
    time.sleep(30)
