# Onion Encoding

It's not about what's on the surface. This flag is layered, and
you'll have to peel it back one step at a time. The first layer is
an obvious one, but what comes next will require a more
creative approach.

## Solution

1. The flag is wrapped in multiple layers of encoding (the "onion").
2. Sequentially decode the data using various schemes: Base64, Base32, Hex, ASCII Decimal, etc.
3. Use the recursive `script.py` to peel back the layers until the flag is found.

## Flag

`CSC26{d06e756065b877da6e810f6d4503a9079318c150}`
