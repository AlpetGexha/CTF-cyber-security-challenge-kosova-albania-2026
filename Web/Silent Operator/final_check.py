import requests
from bs4 import BeautifulSoup
import re
import json

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWlwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Add browser-like headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

print("[+] Fetching dashboard with browser headers...")
response = session.get(f"{base_url}/dashboard", headers=headers)
print(f"Status: {response.status_code}\n")

# Check for any dynamic content or hidden divs
soup = BeautifulSoup(response.text, 'html.parser')

# Look for hidden elements
print("[*] Checking for hidden elements...")
for tag in soup.find_all(style=re.compile(r'display\s*:\s*none', re.I)):
    print(f"[+] Found hidden element: {tag.name}")
    print(f"    Content: {tag.get_text()}")
    if "CSC26{" in tag.get_text():
        print(f"\n🚩 FLAG IN HIDDEN ELEMENT!")

# Check all data attributes
print("\n[*] Checking data- attributes...")
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if attr.startswith('data-'):
            print(f"    {tag.name}.{attr} = {value}")
            if "CSC26{" in str(value):
                print(f"\n🚩 FLAG IN DATA ATTRIBUTE!")

# Fetch app.js again with browser headers
print("\n[+] Fetching app.js with browser headers...")
js_response = session.get(f"{base_url}/static/js/app.js", headers=headers)
print("JavaScript content:")
print(js_response.text)
print()

# Check if there's any other response
print("\n[+] Checking all script sources...")
for script in soup.find_all('script', src=True):
    src = script['src']
    if not src.startswith('http'):
        src = f"{base_url}{src}"
    print(f"[*] Fetching: {src}")
    r = session.get(src, headers=headers)
    print(f"    Content: {r.text}")
    if "CSC26{" in r.text:
        print(f"\n🚩🚩🚩 FLAG IN SCRIPT!")
        flags = re.findall(r'CSC26\{[^}]+\}', r.text)
        print(f"🚩 {flags}")

print("\n[!] RECOMMENDATION:")
print("Since the Python scripts haven't found the flag yet, try:")
print("1. Open https://poiuytrewqas-csc26.cybersecuritychallenge.al/dashboard in Chrome/Firefox")
print("2. Press F12 to open Developer Tools")
print("3. Go to the Console tab")
print("4. Look for any messages or try typing: document.body.innerHTML")
print("5. Check the Network tab for any XHR/Fetch requests")
print("6. Check the Application/Storage tab for localStorage/sessionStorage")
