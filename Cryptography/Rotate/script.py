import string

def rotate(text, shift):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        elif char.islower():
            result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def solve():
    file_path = 'encrypted_rotate.txt'
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print("File not found.")
        return

    print(f"Original: {content}")
    print("-" * 20)
    
    # Try all 26 shifts
    for i in range(26):
        shifted = rotate(content, i)
        # We are looking for the flag format CSC26
        if "CSC26" in shifted:
            print(f"Shift {i}: {shifted}  <-- LIKELY FLAG")
        else:
            print(f"Shift {i}: {shifted}")

if __name__ == "__main__":
    solve()
