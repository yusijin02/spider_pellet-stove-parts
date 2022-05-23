import requests
import base64
import time
import random

def getIP():
    url = "your get ip API"
    res = requests.get(url)
    time.sleep(0.5)
    return res.text

def baseCode(username, password):
    str = base64.b64encode(username + ":" +password)
    return str

def fakeIPGet(url):
    ip = fakeIPGet.ip
    username = 'your username'
    password = 'your password'
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
    }
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ip},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": ip}
    }
    try:
        response = requests.get(url, proxies=proxies, headers=headers)
        return response
    except Exception as e:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("[" + t + "]在代理ip " + ip + "处产生异常，正在重试...", 'str(Exception):\t', str(Exception), 'str(e):\t\t', str(e))
        time.sleep(random.random() * 5)
        fakeIPGet.ip = getIP()
        return fakeIPGet(url)

