def get_yesterday():
    import datetime

    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    yesterday = today - delta
    yesterdaystr = yesterday.strftime('%Y-%m-%d')
    return yesterdaystr


def parse_response(response):
    from bs4 import BeautifulSoup

    datas = {}
    soup = BeautifulSoup(response.text, 'html.parser')
    ul = soup.find('ul', class_='dataul')
    for li in ul.find_all('li'):
        if not li.get('class') == ['datali']:
            continue

        position = li.find('div', class_='divname').text.strip()
        divval = li.find('div', class_='divval')
        value = divval.find('span', class_='label').text.strip()
        showtime = divval.find('span', class_='showtime').text.strip()
        if showtime == get_yesterday():
            info = 'normal'
        else:
            info = 'abnormal'
        datas[position] = (value, showtime, info)
    return datas


def get_radiation_level(url, headers):
    import requests

    response = requests.get(url,  headers=headers)
    if response.status_code != 200:
        print("Error", response.status_code, response.text)
        exit(1)

    datas = parse_response(response)
    if datas == {}:
        return "Empty data"

    message = ''
    for key, value in datas.items():
        message += '['+value[2] + ']\t' + key + \
            ':\t' + value[0]+'\t' + value[1] + '\n'
    return message


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


if __name__ == '__main__':
    url = 'https://data.rmtc.org.cn/gis/listsation0_93M.html'
    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Cache-Control': 'max-age=0',
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Host': "data.rmtc.org.cn",
        'Referer': 'https://data.rmtc.org.cn/gis/listtype0M.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        'X-Requested-With': "XMLHttpRequest",
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile': "?0",
        'Sec-Ch-Ua-Platform': "Windows",
    }
    message = get_radiation_level(url, headers)
    message += 'Refer: '+url+'\n'
    send_email(message)
