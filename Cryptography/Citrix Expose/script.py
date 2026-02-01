import binascii
import os

def decode_ap_nibbles(text):
    # Mapping A->0, B->1, ..., P->15
    # Since 'A' is 65. val = ord(c) - 65.
    
    # Try Big Endian Nibbles (First char is high nibble)
    bytes_be = []
    for i in range(0, len(text), 2):
        if i+1 < len(text):
            hi = ord(text[i]) - ord('A')
            lo = ord(text[i+1]) - ord('A')
            val = (hi << 4) | lo
            bytes_be.append(val)
            
    # Try Little Endian Nibbles (First char is low nibble)
    bytes_le = []
    for i in range(0, len(text), 2):
        if i+1 < len(text):
            lo = ord(text[i]) - ord('A')
            hi = ord(text[i+1]) - ord('A')
            val = (hi << 4) | lo
            bytes_le.append(val)
            
    return bytes_be, bytes_le

def try_xor(bytes_data, key):
    return bytes([b ^ key for b in bytes_data])

def solve():
    file_path = os.path.join(os.path.dirname(__file__), 'encrypted (4).txt')
    with open(file_path, 'r') as f:
        content = f.read().strip()
        
    print(f"Content: {content[:30]}...")

    bytes_be, bytes_le = decode_ap_nibbles(content)
    
    # 1. Check direct decode
    print("\n--- Direct Decode (High Nibble First) ---")
    try:
        print(bytes(bytes_be).decode('utf-8', errors='ignore'))
    except: pass

    print("\n--- Direct Decode (Low Nibble First) ---")
    try:
        print(bytes(bytes_le).decode('utf-8', errors='ignore'))
    except: pass
    
    # 2. Check XOR 0xA5 (Classic Citrix)
    print("\n--- XOR 0xA5 (High Nibble First) ---")
    xored_be = try_xor(bytes_be, 0xA5)
    try:
        print(xored_be)
        print("Text:", xored_be.decode('utf-8', errors='ignore'))
    except: pass
    
    print("\n--- XOR 0xA5 (Low Nibble First) ---")
    xored_le = try_xor(bytes_le, 0xA5)
    try:
        print(xored_le)
        print("Text:", xored_le.decode('utf-8', errors='ignore'))
    except: pass
    
    # 3. Check simple ROL/ROR or other XORs
    # Often Citrix is just XOR with previous byte or something?
    
    # 4. Brute force single byte XOR
    print("\n--- Brute Force XOR (High Nibble First) ---")
    found_flag = False
    for k in range(256):
        x = try_xor(bytes_be, k)
        try:
            s = x.decode('utf-8')
            if "CSC" in s or "flag" in s or "Citrix" in s:
                print(f"Key {k:02x}: {s}")
                found_flag = True
        except:
            pass
            
    print("\n--- Brute Force XOR (Low Nibble First) ---")
    for k in range(256):
        x = try_xor(bytes_le, k)
        try:
            s = x.decode('utf-8')
            if "CSC" in s or "flag" in s or "Citrix" in s:
                print(f"Key {k:02x}: {s}")
                found_flag = True
        except:
            pass

if __name__ == "__main__":
    solve()
