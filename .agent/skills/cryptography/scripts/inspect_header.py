
import os

file_path = 'c:/Users/agexh/Desktop/ctf/Dedective/USB e Enkriptuar/communications.enc'

try:
    with open(file_path, 'rb') as f:
        content = f.read(1000)
        print("--- HEX ---")
        print(content.hex()[:200]) # First 100 bytes as hex
        print("\n--- RAW (repr) ---")
        print(repr(content))
        try:
            print("\n--- DECODED (UTF-8) ---")
            print(content.decode('utf-8'))
        except:
            print("\n--- CANNOT DECODE FULLY AS UTF-8 ---")
            # Try decoding strictly the beginning until it fails
            sys.stdout.buffer.write(content) # Write raw bytes to stdout if possible, or just skip
except Exception as e:
    print(f"Error: {e}")
