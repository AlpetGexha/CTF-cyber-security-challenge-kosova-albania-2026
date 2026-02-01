
import re
import sys

file_path = 'c:/Users/agexh/Desktop/ctf/Dedective/USB e Enkriptuar/communications.enc'

with open(file_path, 'rb') as f:
    content = f.read()

# Try to find N
decoded = content[:4000].decode('utf-8', errors='ignore')
n_match = re.search(r'Modulus \(n\): (\d+)', decoded)
if not n_match:
    print("Error: Could not find n")
    sys.exit(1)

n_str = n_match.group(1)
n = int(n_str)

with open('n.txt', 'w') as f_n:
    f_n.write(n_str)

# Find data start
# Look for the closing box line ╚════...
# ╚ is \xe2\x95\x9a in UTF-8
box_corner = b'\xe2\x95\x9a' 
idx_corner = content.rfind(box_corner, 0, 4000) # Search in first 4KB

if idx_corner == -1:
    print("Could not find closing box corner, fallback to manual offset from 'Articles'...")
    # fallback logic if needed
    end_marker = b'Articles 293-297 (Computer Crimes).'
    idx = content.find(end_marker)
    if idx == -1:
         print("Critical Error: markers not found")
         sys.exit(1)
    # Search for next newline after this
    header_end = content.find(b'\n', idx + len(end_marker)) + 1
else:
    # Found corner. Find the end of this line (newline)
    header_end = content.find(b'\n', idx_corner) + 1

# Extract ciphertext
ciphertext = content[header_end:]

# But wait, there might be newlines between the box and the data?
# Let's strip leading whitespace from ciphertext just in case it's text? 
# No, it's encrypted binary. It shouldn't have leading whitespace unless accidental.
# However, if there are extra newlines after the header, we should skip them.
# A safe bet is to skip any sequence of \r or \n immediately following the header line.

while True:
    if header_end < len(content) and content[header_end] in (10, 13): # \n or \r
        header_end += 1
    else:
        break

ciphertext = content[header_end:]

print(f"Ciphertext starts at offset {header_end}, length {len(ciphertext)}")

with open('ciphertext.bin', 'wb') as f_c:
    f_c.write(ciphertext)
