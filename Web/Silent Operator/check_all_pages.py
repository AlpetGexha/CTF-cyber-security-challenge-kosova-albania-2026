import requests
from bs4 import BeautifulSoup
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

pages = ["/", "/register", "/login"]

for page in pages:
    url = f"{base_url}{page}"
    print(f"\n{'='*70}")
    print(f"[+] Checking: {url}")
    print('='*70)
    
    response = session.get(url)
    print(f"Status: {response.status_code}\n")
    
    # Show full HTML
    print(response.text)
    print("\n")
    
    # Look for flag
    flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
    if flags:
        print(f"\n🚩🚩🚩 FLAG FOUND ON {page}!")
        print(f"🚩 {flags}")
