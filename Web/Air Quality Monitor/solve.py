import string

text = "ACBFEEEGGDGAGOLACBOEACTYGFLEKOLEEEEPPCLS"

for shift in range(26):
    result = ""
    for c in text:
        if c.isalpha():
            result += chr((ord(c) - 65 + shift) % 26 + 65)
        else:
            result += c
    print(shift, result)
