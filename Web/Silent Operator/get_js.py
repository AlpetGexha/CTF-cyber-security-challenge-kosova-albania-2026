import requests
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

print("[+] Fetching /static/js/app.js...")
js_url = f"{base_url}/static/js/app.js"
response = session.get(js_url)
print(f"[+] Status: {response.status_code}\n")

if response.status_code == 200:
    print("[+] JavaScript content:")
    print("="*60)
    print(response.text)
    print("="*60)
    
    # Look for flags
    flag_patterns = [r'CSC26\{[^}]+\}', r'CTF\{[^}]+\}', r'FLAG\{[^}]+\}', r'flag\{[^}]+\}']
    for pattern in flag_patterns:
        matches = re.findall(pattern, response.text, re.IGNORECASE)
        if matches:
            print(f"\n🚩🚩🚩 [!!!] FLAG FOUND: {matches} 🚩🚩🚩")
