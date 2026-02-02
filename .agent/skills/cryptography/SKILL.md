---
name: Cryptography Specialist
description: A specialized skill for identifying, analyzing, and breaking encryption schemes, with a focus on RSA, XOR, and classical ciphers.
---

# Cryptography Specialist Skill

This skill equips the agent with the ability to analyze encrypted files, identifying encryption types, and apply mathematical attacks to recover plaintext.

## Capabilities

1.  **Encryption Identification**
    - Analyze file headers (magic bytes, PEM formats).
    - Identify encryption algorithms (RSA, AES, XOR, etc.).
    - Detect encoding schemes (Base64, Hex, PEM, Rot13).

2.  **RSA Attacks**
    - **Small Public Exponent Attack (`e=3`)**: Cube root attack.
    - **Wiener's Attack**: Use when the private exponent `d` is small.
    - **Pollard's p-1**: Use when `p-1` has small prime factors.
    - **Factorization**: Use `factor_tool.py` or online DBs (factordb.com) to find `p` and `q`.

3.  **XOR & Stream Ciphers**
    - **Multi-Byte XOR**: Determining key length (Hamming distance) and brute-forcing the key.
    - **Known Plaintext Attack**: `Cipher ^ Known_Plain = Key`.
    - **LFSR (Linear Feedback Shift Registers)**: Analyzing bit streams using `z3` or Berlekamp-Massey algorithm.

4.  **Bytecode & Obfuscation**
    - **PYC Decompilation**: Handling `.pyc` files using `uncompyle6` or `decompyle3`.
    - **Bitwise Reversal**: Reversing custom scrambling logic found in source code.

## Workflow

### Step 1: Analyze the Artifact

Inspect the file to understand what you are dealing with.

- **Headers**: `python scripts/inspect_header.py <file>`
- **PEM Files**: Extract `n` and `e`.
- **Blob**: Calculate entropy. High entropy = Encrypted/Compressed. Low Entropy = Text/Encoding.

### Step 2: Determine Attack Vector

- **RSA**: Check `n` size and `e` value.
- **Binary Blob + "XOR" hint**: Try `xortool` logic or brute-force single byte XOR.
- **Python Script**: If provided logic, reimplement the _inverse_ logic.
  - If math is complex, use `z3` solver.

### Step 3: Execute Attack

Select the appropriate script from the toolkit:

- **Wiener's/Pollard**: Use provided `./scripts/` tools.
- **XOR Solver**:
  ```python
  from itertools import cycle
  def xor(data, key):
      return bytes([a ^ b for a, b in zip(data, cycle(key))])
  ```

### Step 4: Verification

- Ensure the decrypted output makes sense (e.g., matching flag format `Detective{...}` or readable text).
- If "garbage" output, check for subsequent layers of encryption.

## Available Scripts (in ./scripts/)

- `extract_n.py`: Extracts modulus and exponent from PEM files.
- `factor_tool.py`: Interfaces with FactorDB and local algorithms to factor `n`.
- `wiener.py`: Implements Wiener's attack for small `d`.
- `pollard.py`: Implements Pollard's p-1 factorization.
