import requests
import gzip
import base64

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
}

print("[+] Fetching app.js...")
response = session.get(f"{base_url}/static/js/app.js", headers=headers)
print(f"Status: {response.status_code}")
print(f"Content-Encoding: {response.headers.get('Content-Encoding', 'none')}")
print(f"Content-Length: {len(response.content)}")
print(f"Response headers: {dict(response.headers)}\n")

# The content might be gzip compressed
print("[+] Raw bytes (first 100):")
print(response.content[:100])
print()

print("[+] Decoded content:")
print(response.text)
print()

# Try without Accept-Encoding
print("\n[+] Fetching without Accept-Encoding...")
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
response2 = session.get(f"{base_url}/static/js/app.js", headers=headers2)
print(f"Content: {response2.text}")

# Look for flag
import re
if re.search(r'CSC26\{[^}]+\}', response2.text, re.IGNORECASE):
    print(f"\n🚩🚩🚩 FLAG FOUND!")
    flags = re.findall(r'CSC26\{[^}]+\}', response2.text, re.IGNORECASE)
    print(f"🚩 {flags}")
