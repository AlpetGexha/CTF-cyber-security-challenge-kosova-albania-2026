import requests

url = "https://poiuytrewqazx-csc26.cybersecuritychallenge.al/analizo"
data = {"url": "http://example.com", "submit": "Analizo"}

print(f"POSTing to {url}...")
# Note: Usually forms are x-www-form-urlencoded, requests handles this with 'data' param
r = requests.post(url, data=data, allow_redirects=True)

print(f"Status Code: {r.status_code}")
print(f"URL: {r.url}") # Did it redirect?
print(f"Length: {len(r.content)}")

with open("post_result.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("Saved post_result.html")
print("-" * 20)
print(r.text[:2000])
