
def solve_drunken():
    # Define keyboard rows (standard US QWERTY)
    # Both normal and shifted
    rows = [
        r"`1234567890-=",
        r"~!@#$%^&*()_+",
        "qwertyuiop[]\\",
        "QWERTYUIOP{}|",
        r"asdfghjkl;'",
        r'ASDFGHJKL:"',
        r"zxcvbnm,./",
        r"ZXCVBNM<>?"
    ]

    try:
        with open('encrypted_text.txt', 'r') as f:
            encrypted = f.read().strip()
    except FileNotFoundError:
        print("encrypted_text.txt not found.")
        return

    print(f"Encrypted: {encrypted}")

    decrypted = []
    for char in encrypted:
        found = False
        for row in rows:
            if char in row:
                index = row.find(char)
                if index > 0:
                    decrypted.append(row[index - 1])
                    found = True
                    break
                else:
                    # If it's the first char in row, maybe wrap around or it's an error?
                    # But based on the problem description "missed", they probably hit key to the right.
                    # So we take left. If index 0, there is no key to the left.
                    # We'll just keep it? Or assume it's not possible?
                    decrypted.append(char)
                    found = True
                    break
        if not found:
            decrypted.append(char)

    result = "".join(decrypted)
    print(f"Decrypted: {result}")

if __name__ == "__main__":
    solve_drunken()
