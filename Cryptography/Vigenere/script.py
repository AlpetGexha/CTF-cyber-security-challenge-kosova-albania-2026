def decrypt_vigenere(ciphertext, key, skip_non_alpha_index=True):
    plaintext = []
    key_length = len(key)
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % key_length]
            key_shift = ord(key_char.lower()) - ord('a')
            
            decrypted_char = chr((ord(char) - base - key_shift) % 26 + base)
            plaintext.append(decrypted_char)
            
            key_index += 1
        else:
            plaintext.append(char)
            if not skip_non_alpha_index:
                key_index += 1
    
    return "".join(plaintext)

def solve():
    key = "password"
    cipher_line = "RSU26{9x4225a3s9s8g33t0a0v7t5b5p5r99i1t7a1w0t9}"
    
    print(f"Cipher: {cipher_line}")
    print(f"Key:    {key}")
    
    # Method 1: Standard (skip non-alpha for index)
    res1 = decrypt_vigenere(cipher_line, key, skip_non_alpha_index=True)
    print(f"\nMethod 1 (Standard): {res1}")

    # Method 2: Don't skip non-alpha for index
    res2 = decrypt_vigenere(cipher_line, key, skip_non_alpha_index=False)
    print(f"Method 2 (Index all): {res2}")
    
    # Check other keys starting with PAS
    other_keys = ["passport", "passcode", "passphrase", "passing"]
    for k in other_keys:
        r = decrypt_vigenere(cipher_line, k, skip_non_alpha_index=True)
        # print(f"Try {k}: {r}")

if __name__ == "__main__":
    solve()
