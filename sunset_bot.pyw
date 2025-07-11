import os
import sys
from time import sleep
import requests
import logging
from datetime import datetime
from config_loader import read_config_byconfigparser

is_online = read_config_byconfigparser('COMMON','is_online')
filename =  os.path.basename(__file__)
if not is_online:
    # backup_directory = read_config_byconfigparser('PATH','backup_directory')
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
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

if len(sys.argv) != 2 or sys.argv[1] not in ('afternoon', 'evening'):
    print("Usage: python3 sunset_bot.py [afternoon|evening]")
    sys.exit(1)

mode = sys.argv[1]

base_url = "https://sunsetbot.top/"
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
            headers = {
                "Host": "sunsetbot.top",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
                "Accept": "*/*",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-HK;q=0.6,en-US;q=0.4,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "X-Requested-With": "XMLHttpRequest",
                "DNT": "1",
                "Sec-GPC": "1",
                "Connection": "keep-alive",
                "Referer": "https://sunsetbot.top/",
                "Cookie": "city_name=\344\270\212\346\265\267",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=0",
                "TE": "trailers",
            }
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            judge = data.get("tb_quality", None)
            if not judge or float(judge.split("（")[0]) < 0.2:
                raise ValueError(f"Quality for {event} is too low: {judge}")

            results["judge"] = True
            results[event] = {
                "date": data.get("tb_event_time", "").replace("<br>", " ").strip(),
                "quality": data.get("tb_quality", "").replace("<br>", " ").strip(),
                "aod": data.get("tb_aod", "").replace("<br>", " ").strip(),
            }
        except Exception as e:
            logging.warning(f"fetching bad data for {event}: {e}")
            results[event] = {"bad": str(e).strip()}
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
        if "bad" in data:
            email_content.extend([
                f"\n[{event}] 无效",
                f"{data['bad']}",
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

    print(message)
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except smtplib.SMTPResponseException as e:
        if e.smtp_code == -1 and e.smtp_error == b'\x00\x00\x00':
            print("Ignoring specific SMTP response exception")
        else:
            print(f"SMTP error: {e.smtp_code} - {e.smtp_error}")
    except Exception as e:
        print(f"Error sending email: {e}")

citys = read_config_byconfigparser(filename,'citys')
for city in citys:
    logging.info(f"Starting {mode} task for city {city} at {datetime.now()}")

    res = fetch_sun_data(true_events, city)
    print(res)
    if not res['judge']:
        logging.warning(f"No valid data for {city} at {datetime.now()}")
        continue
    del res['judge']
    send_email(generate_email_content(city, res))
    logging.info(f"Email sent successfully for {city} at {datetime.now()}")
