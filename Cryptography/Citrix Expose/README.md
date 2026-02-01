# Citrix Expose

The corporate gateway uses a proprietary encryption scheme
to 'protect' its session tokens. Your mission is to investigate
the token provided and figure out how to recover the hidden
message inside. Citrix may call it secure, but can you prove
otherwise?

## Solution

1. Decode the custom encoding where pairs of letters 'A'-'P' represent high and low nibbles.
2. Extract every second byte (odd indices).
3. Apply a differential XOR decoding (current byte XOR previous byte) to recover the plaintext.
4. Run `script.py`.

## Flag

`CSC26{d6a183df7b5d7fad5cf63ffcd37dbf7187ed7d0e}`
