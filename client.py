import requests
import os
import sys

s = requests.session()
PROXY = None

if not os.path.exists('data'):
    os.mkdir('data')

with open('settings/settings.ini', 'r') as f:
    for data in f:
        if data == "User-Proxy":
            if len(data.split(':', 1)[1]) > 5:
                PROXY = data.split(':', 1)[1]

if PROXY:
    s.proxies.update({'http': f'http://{PROXY}', 'https': f'https://{PROXY}'})

def checkAvailability():
    with open('data/username_check.txt', 'r') as f:
        for data in f:
            _Data = {'method': 'checkAvailability', 'username': data.strip().lower()}
            _Headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
                        'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                        'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest',
                        'Origin': 'http://www.neopets.com', 'DNT': '1'}
            resp = s.post('http://www.neopets.com/signup/ajax.phtml', data=_Data, headers=_Headers)
            if 'is available!' in resp.text:
                print(f'[+] {data.strip()} is available!')
                saveUsernames(data.strip())

def saveUsernames(user):
    _Used = False
    with open('data/available_usernames.txt', 'r') as f:
        for data in f:
            if data == user:
                _Used = True
    if not _Used:
        with open('data/available_usernames.txt', 'a') as f:
            f.write(f'{user}\n')

checkAvailability()