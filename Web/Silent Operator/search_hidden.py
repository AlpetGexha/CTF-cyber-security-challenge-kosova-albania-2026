import requests
from bs4 import BeautifulSoup, Comment
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Get dashboard
print("[+] Checking dashboard for hidden content...")
response = session.get(f"{base_url}/dashboard")
soup = BeautifulSoup(response.text, 'html.parser')

# Check for HTML comments
print("\n[*] HTML Comments:")
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for comment in comments:
    print(f"    <!-- {comment} -->")
    if "CSC26{" in str(comment):
        print(f"\n🚩 FLAG IN COMMENT: {comment}")

# Check all attributes for hidden data
print("\n[*] Checking all element attributes...")
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if isinstance(value, str) and ("CSC26{" in value or "flag" in value.lower()):
            print(f"    {tag.name}.{attr} = {value}")

# Check for base64 encoded content
print("\n[*] Looking for base64/encoded content...")
import base64
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if isinstance(value, str) and len(value) > 20:
            try:
                decoded = base64.b64decode(value).decode('utf-8', errors='ignore')
                if "CSC26{" in decoded or "flag" in decoded.lower():
                    print(f"    Found in {tag.name}.{attr}:")
                    print(f"        Encoded: {value}")
                    print(f"        Decoded: {decoded}")
            except:
                pass

# Try searching for specific terms
print("\n[*] Searching for various terms...")
search_url = f"{base_url}/search"
terms = ["enjoyer", "Fellow", "box", "container", "docker", "trap", "free", "bound", "arcade", "library"]

for term in terms:
    response = session.post(search_url, data={"q": term})
    if "No results" not in response.text:
        print(f"\n[+] Results for '{term}':")
        soup = BeautifulSoup(response.text, 'html.parser')
        main = soup.find('main')
        if main:
            print(main.get_text())
        # Check for flag
        if re.search(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE):
            print(f"\n🚩🚩🚩 FLAG FOUND!")
            flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
            print(f"🚩 {flags}")
