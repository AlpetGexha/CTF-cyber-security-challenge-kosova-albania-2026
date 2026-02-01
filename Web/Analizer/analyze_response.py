import requests

url = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/"
params = {"url": "http://example.com", "submit": "Analizo"}

print("Requesting...")
r = requests.get(url, params=params)

print(f"Status Code: {r.status_code}")
print(f"Content Type: {r.headers.get('Content-Type')}")
print(f"Length: {len(r.content)}")

with open("result.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved result.html")
print("First 1000 chars:")
print(r.text[:1000])

# Check for image tag
if "<img" in r.text:
    print("\n[+] Found image tag in response!")
else:
    print("\n[-] No image tag found.")
