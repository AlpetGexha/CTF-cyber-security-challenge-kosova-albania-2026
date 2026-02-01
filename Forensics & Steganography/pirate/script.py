from PIL import Image
import base64

def extract_lsb(path):
    img = Image.open(path)
    pixels = img.load()
    w, h = img.size

    bits = []
    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y][:3]
            bits.extend([r & 1, g & 1, b & 1])

    return bytes(
        int("".join(map(str, bits[i:i+8])), 2)
        for i in range(0, len(bits), 8)
        if len(bits[i:i+8]) == 8
    )

data = extract_lsb("stego_image.png").decode("utf-8", errors="ignore")

if "======" in data:
    payload = data.split("======")[0] + "======"
    payload = "".join(c for c in payload if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567=")
    flag = base64.b32decode(payload).decode("utf-8", errors="ignore")
    print(flag)
