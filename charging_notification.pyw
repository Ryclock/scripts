import time
from email.mime.text import MIMEText
import smtplib
import subprocess
import sys
import os
from config_loader import read_config_byconfigparser

filename = os.path.basename(__file__)
sender_email = read_config_byconfigparser('MAIL', 'sender_email')
sender_password = read_config_byconfigparser(filename, 'sender_password')
receiver_email = read_config_byconfigparser('MAIL', 'receiver_email')
subject = read_config_byconfigparser(filename, 'subject')
smtp_server = read_config_byconfigparser('MAIL', 'smtp_server')
smtp_port = read_config_byconfigparser('MAIL', 'smtp_port')
duration = read_config_byconfigparser(filename, 'duration_seconds')

try:
    import psutil
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

previous_status = psutil.sensors_battery().power_plugged
start_time = time.time()
while time.time() - start_time < duration:
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
    time.sleep(10)
