import requests
from bs4 import BeautifulSoup
import re
import json

# Base URL
base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"

# Create session
session = requests.Session()

# Try to access dashboard with the provided session cookie
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

print("[+] Accessing dashboard...")
dashboard_url = f"{base_url}/dashboard"
response = session.get(dashboard_url)
print(f"[+] Dashboard status: {response.status_code}\n")

# Search for "javascript" since the hint mentions JavaScript
search_url = f"{base_url}/search"
queries = ["javascript", "js", "script", "code", "flag", ""]

for query in queries:
    print(f"\n{'='*60}")
    print(f"[*] Searching for: '{query}'")
    print(f"{'='*60}")
    
    response = session.post(search_url, data={"q": query})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract all script tags
    scripts = soup.find_all('script')
    if scripts:
        print(f"\n[+] Found {len(scripts)} script tag(s)")
        for i, script in enumerate(scripts):
            if script.string and script.string.strip():
                print(f"\n--- Script {i+1} ---")
                print(script.string)
                
                # Look for flag patterns
                flag_patterns = [r'CSC26\{[^}]+\}', r'CTF\{[^}]+\}', r'FLAG\{[^}]+\}', r'flag\{[^}]+\}']
                for pattern in flag_patterns:
                    matches = re.findall(pattern, script.string)
                    if matches:
                        print(f"\n🚩 [!] FLAG FOUND: {matches}")
                        
    # Check for inline event handlers
    for tag in soup.find_all(True):
        for attr in ['onclick', 'onload', 'onerror', 'onmouseover']:
            if tag.get(attr):
                print(f"\n[+] Found {attr}: {tag.get(attr)}")
    
    # Print text content
    print(f"\n[*] Page text content:")
    print(soup.get_text()[:500])
    
    # Look for flags in full HTML
    flag_patterns = [r'CSC26\{[^}]+\}', r'CTF\{[^}]+\}', r'FLAG\{[^}]+\}']
    for pattern in flag_patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        if matches:
            print(f"\n🚩🚩🚩 [!!!] FLAG FOUND IN HTML: {matches} 🚩🚩🚩")

print("\n\n[*] Complete HTML of last search:")
print(response.text)
