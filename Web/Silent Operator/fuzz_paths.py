import requests
from concurrent.futures import ThreadPoolExecutor
import re

base_url = "https://poiuytrewqas-csc26.cybersecuritychallenge.al"
session = requests.Session()
session.cookies.set('session', 'eyJ1c2VyIjoiYWxwZXRnIn0.aXymyw.GBEYMO9Mn9kpHr1J86YGyGs4CsE')

# Common web paths
paths = [
    "/api", "/api/flag", "/api/config", "/api/users",
    "/console", "/debug", "/test",
    "/config", "/config.json", "/package.json",
    "/flag", "/flag.txt", "/secret", "/admin",
    "/.env", "/.git/HEAD", "/.git/config",
    "/backup", "/backup.zip", "/source.zip",
    "/debug/flag", "/debug/config",
    "/users", "/user/alpetg",
    "/profile", "/settings",
    "/search/flag", "/search/admin",
    "/static/flag.txt", "/static/secret.txt",
    "/downloads", "/uploads",
    "/data", "/data.json",
]

print("[+] Checking for hidden paths...")
def check_path(path):
    url = f"{base_url}{path}"
    try:
        response = session.get(url, timeout=5)
        if response.status_code == 200:
            print(f"\n[+] Found {path} (Status: 200)")
            print(f"    Content length: {len(response.text)}")
            print(f"    First 200 chars: {response.text[:200]}")
            
            # Check for flag
            if re.search(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE):
                print(f"\n🚩🚩🚩 FLAG FOUND AT {path}!")
                flags = re.findall(r'CSC26\{[^}]+\}', response.text, re.IGNORECASE)
                print(f"🚩 {flags}")
                return True
        elif response.status_code not in [404, 405]:
            print(f"[*] {path}: Status {response.status_code}")
    except:
        pass
    return False

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(check_path, paths))

if any(results):
    print("\n[!] Flag found!")
else:
    print("\n[*] No hidden paths with flag found")
