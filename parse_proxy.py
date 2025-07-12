from datetime import datetime
import requests
import ruamel.yaml
import socks
import socket
import sys

if len(sys.argv) != 2:
    print(f"Usage: python3 {__file__} <target_url>")
    sys.exit(1)

target_url = str(sys.argv[1])
if not target_url.startswith("http"):
    target_url = "http://"+target_url

today = datetime.now().strftime('%Y%m%d')
print("today: "+today)
url=f"https://free.datiya.com/uploads/{today}-clash.yaml"
print("url: "+url)
response = requests.get(url)
response.raise_for_status()

yaml = ruamel.yaml.YAML()
yaml_content = response.content.decode('utf-8')
data = yaml.load(yaml_content)

expected_proxy = None
for proxy in data['proxies']:
    expected_proxy = proxy
    proxy_name = expected_proxy['name']
    print(f"\n正在测试代理: {proxy_name}")
    proxy_type = expected_proxy['type']
    proxy_server = expected_proxy['server']
    proxy_port = expected_proxy['port']

    if proxy_type == 'ss':
        # Shadowsocks 代理
        proxy_url = f"socks5://{proxy_server}:{proxy_port}"
        if 'password' in expected_proxy and 'cipher' in expected_proxy:
            proxy_url = f"socks5://{expected_proxy['cipher']}:{expected_proxy['password']}@{proxy_server}:{proxy_port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    elif proxy_type == 'trojan':
        # Trojan 代理
        socks.set_default_proxy(socks.SOCKS5, proxy_server, proxy_port)
        if 'password' in expected_proxy:
            socks.set_default_proxy(socks.SOCKS5, proxy_server, proxy_port,
                                    username=expected_proxy['password'], password='')
        socket.socket = socks.socksocket
        proxy_url = f"socks5://{proxy_server}:{proxy_port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    else:
        print(f"{proxy_name}是不支持的代理类型: {proxy_type}")
        expected_proxy=None
        continue

    try:
        # 使用代理发送请求
        test_response = requests.get(target_url, proxies=proxies, timeout=10)
        test_response.raise_for_status()
        break
    except requests.RequestException as e:
        print(f"请求失败: {e}")
        expected_proxy=None

if expected_proxy:
    print(f"预期使用的代理: {proxy_name}")
else:
    print("没有找到有效的代理")