import requests
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Check CSS file
print("[+] Checking CSS file...")
css_url = f"{base_url}/static/css/retro.css"
response = session.get(css_url)
print(f"Status: {response.status_code}\n")
print(response.text)
print("\n" + "="*60)

# Look for flag in CSS
if re.search(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE):
    print("\n🚩🚩🚩 FLAG FOUND IN CSS!")
    flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
    print(f"🚩 {flags}")
