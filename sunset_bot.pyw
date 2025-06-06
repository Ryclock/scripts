import os
import sys
from time import sleep
import requests
import logging
from datetime import datetime
from config_loader import read_config_byconfigparser

# backup_directory = read_config_byconfigparser('PATH','backup_directory')
filename =  os.path.basename(__file__)
sub_id = read_config_byconfigparser(filename,'sub_id')
# backup_directory = os.path.join(backup_directory, sub_id)
# if not os.path.exists(backup_directory):
#     os.makedirs(backup_directory)
#     logging.info(f"create directory '{backup_directory}' for backup")

log_directory = read_config_byconfigparser('PATH','log_directory')
log_file = os.path.join(log_directory, sub_id)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_file
)

if len(sys.argv) != 2 or sys.argv[1] not in ('afternoon', 'evening'):
    print("Usage: python3 sunset_bot.py [afternoon|evening]")
    sys.exit(1)

mode = sys.argv[1]

city = read_config_byconfigparser(filename,'city')
logging.info(f"Starting {mode} task for city {city} at {datetime.now()}")

base_url = read_config_byconfigparser(filename,'base_url')
events = read_config_byconfigparser(filename, 'events')
true_events = events[mode] if events else []

def fetch_sun_data(events, city, base_url=base_url):
    results = {'judge':False}

    for event in events:
        params = {
            "intend": "select_city",
            "query_city": city,
            "event": event
        }
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            judge = data.get("tb_quality", None)
            if not judge or float(judge.split("<br>")[0]) < 0.2:
                raise ValueError(f"Quality for {event} is too low: {judge}")

            results["judge"] = True
            results[event] = {
                "date": data.get("tb_event_time", "").replace("<br>", " ").strip(),
                "quality": data.get("tb_quality", "").replace("<br>", " ").strip(),
                "aod": data.get("tb_aod", "").replace("<br>", " ").strip(),
            }
        except Exception as e:
            logging.error(f"Error fetching data for {event}: {e}")
            results[event] = {"error": str(e).strip()}
        finally:
            sleep(10)

    return results

def generate_email_content(city, good_results):
    email_content = [
        f"预报城市: {city}",
        f"数据获取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 15,
    ]

    for event, data in good_results.items():
        if "error" in data:
            email_content.extend([
                f"\n[{event}] 无效",
                f"{data['error']}",
                "-" * 10,
            ])
        else:
            email_content.extend([
                f"\n[{event}] 细节",
                f"时间: {data['date']}",
                f"质量: {data['quality']}",
                f"AOD: {data['aod']}",
                "-" * 10,
            ])

    return "\n".join(email_content)

def send_email(message):
    import sys
    import subprocess
    from email.mime.text import MIMEText
    import smtplib
    import os
    from config_loader import read_config_byconfigparser

    filename = os.path.basename(__file__)
    sender_email = read_config_byconfigparser('MAIL', 'sender_email')
    sender_password = read_config_byconfigparser('MAIL', 'sender_password')
    receiver_email = read_config_byconfigparser('MAIL', 'receiver_email')
    subject = read_config_byconfigparser(filename, 'subject')
    smtp_server = read_config_byconfigparser('MAIL', 'smtp_server')
    smtp_port = read_config_byconfigparser('MAIL', 'smtp_port')

    try:
        import psutil
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "psutil"])
        import psutil

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

res = fetch_sun_data(true_events, city)
print(res)
if not res['judge']:
    logging.warning(f"No valid data for {city} at {datetime.now()}")
    exit(0)
del res['judge']
# send_email(generate_email_content(city, res))
print(generate_email_content(city, res))
logging.info(f"Email sent successfully for {city} at {datetime.now()}")
