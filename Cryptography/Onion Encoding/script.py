import base64
import binascii

def auto_pad_b32(s):
    return s + "=" * ((8 - len(s) % 8) % 8)

def auto_pad_b64(s):
    return s + "=" * ((4 - len(s) % 4) % 4)

def try_decoders(data, step=1):
    print(f"\n--- Step {step} ---")
    extract_preview = data[:50] if len(data) > 50 else data
    print(f"Data start: {extract_preview}...")

    # Check for "CSC26{" or "flag{"
    if "CSC26{" in data or "flag{" in data:
        print("\n\nFOUND FLAG POTENTIALLY:")
        print(data)
        return

    # Try Space Separated Decimals
    # "54 68 53 ..."
    try:
        parts = data.split()
        if all(part.isdigit() for part in parts):
            chars = [chr(int(p)) for p in parts]
            decoded_text = "".join(chars)
            print("Decoded as ASCII Decimal")
            return try_decoders(decoded_text, step + 1)
    except Exception:
        pass

    # Try Base64
    try:
        decoded = base64.b64decode(auto_pad_b64(data))
        decoded_text = decoded.decode('utf-8')
        if not decoded_text.isprintable() and step > 1:
             pass # heuristic to reduce false positives
        else:
             print("Decoded as Base64")
             return try_decoders(decoded_text, step + 1)
    except Exception:
        pass

    # Try Base32
    try:
        decoded = base64.b32decode(auto_pad_b32(data))
        decoded_text = decoded.decode('utf-8')
        print("Decoded as Base32")
        return try_decoders(decoded_text, step + 1)
    except Exception:
        pass

    # Try Hex
    try:
        # cleanup spaces/newlines usually
        clean_data = data.replace(' ', '').replace('\n', '')
        decoded = bytes.fromhex(clean_data)
        decoded_text = decoded.decode('utf-8')
        print("Decoded as Hex")
        return try_decoders(decoded_text, step + 1)
    except Exception:
        pass
    
    # Try Rot13 (only if it looks like letters)
    if step > 1: # don't rot13 original unless obvious
        try:
             import codecs
             rot13 = codecs.decode(data, 'rot13')
             if "CSC26" in rot13 or "flag" in rot13.lower(): # Basic check
                 print("Decoded as Rot13")
                 print(rot13)
                 return
        except:
            pass

    print(f"Stuck at step {step}. Result: {data}")

if __name__ == "__main__":
    with open('encrypted (2).txt', 'r') as f:
        content = f.read().strip()
    
    try_decoders(content)