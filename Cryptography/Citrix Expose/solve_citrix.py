import binascii
import os

def solve():
    file_path = os.path.join(os.path.dirname(__file__), 'encrypted (4).txt')
    with open(file_path, 'r') as f:
        content = f.read().strip()
    
    # Decode A-P
    raw_bytes = []
    for i in range(0, len(content), 2):
        hi = ord(content[i]) - ord('A')
        lo = ord(content[i+1]) - ord('A')
        raw_bytes.append((hi << 4) | lo)
        
    # Extract odd bytes (indices 1, 3, 5...)
    odd_bytes = raw_bytes[1::2]
    
    plain = []
    # P[0] = O[0]
    plain.append(odd_bytes[0])
    
    # P[i] = O[i] ^ O[i-1]
    for i in range(1, len(odd_bytes)):
        p = odd_bytes[i] ^ odd_bytes[i-1]
        plain.append(p)
        
    decoded_text = bytes(plain).decode('utf-8')
    print("Decrypted Flag:")
    # print(repr(decoded_text))
    print(decoded_text)

if __name__ == "__main__":
    solve()
