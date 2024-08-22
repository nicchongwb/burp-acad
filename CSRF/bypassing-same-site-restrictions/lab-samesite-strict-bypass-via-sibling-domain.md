This lab's live chat feature is vulnerable to cross-site WebSocket hijacking (CSWSH). To solve the lab, log in to the victim's account.

To do this, use the provided exploit server to perform a CSWSH attack that exfiltrates the victim's chat history to the default Burp Collaborator server. The chat history contains the login credentials in plain text.

If you haven't done so already, we recommend completing our topic on WebSocket vulnerabilities before attempting this lab. 

References:
- https://portswigger.net/web-security/websockets/cross-site-websocket-hijacking
- https://book.hacktricks.xyz/pentesting-web/websocket-attacks#simple-attack 


# Solution

Chat feature upgrade to WS
```http
GET /chat HTTP/2
Host: 0a2200850478a166807e262300be0031.web-security-academy.net
Connection: Upgrade
Pragma: no-cache
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36
Upgrade: websocket
Origin: https://0a2200850478a166807e262300be0031.web-security-academy.net
Sec-Websocket-Version: 13
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: session=Y0GnHzWsVYWey5AGB1WwqZRxlrbznllk
Sec-Websocket-Key: 08CITasFr2I9/4aorW19Ww==
```
- Response - 101 Switching Protocol
- Only session cookie is sent, no other unpredictable values (eg. CSRF token) is sent to application during WS upgrade

TBC