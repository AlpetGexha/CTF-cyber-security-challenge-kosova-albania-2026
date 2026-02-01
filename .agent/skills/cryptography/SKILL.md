---
name: Cryptography Specialist
description: A specialized skill for identifying, analyzing, and breaking encryption schemes, with a focus on RSA and classical ciphers.
---

# Cryptography Specialist Skill

This skill equips the agent with the ability to analyze encrypted files, identifying encryption types, and apply mathematical attacks to recover plaintext.

## Capabilities

1.  **Encryption Identification**
    - Analyze file headers (magic bytes, PEM formats).
    - Identify encryption algorithms (RSA, AES, XOR, etc.).
    - Detect encoding schemes (Base64, Hex, PEM).

2.  **RSA Attacks**
    - **Small Public Exponent Attack**: Use when `e` is small (e.g., 3).
    - **Wiener's Attack**: Use when the private exponent `d` is small.
    - **Pollard's p-1**: Use when `p-1` has small prime factors.
    - **Factorization**: Use `factor_tool.py` or online DBs (factordb.com) to find `p` and `q` from `n`.

3.  **Tool Usage**
    - The agent has access to a library of python scripts in `./scripts/` to perform these attacks.

## Workflow

### Step 1: Analyze the Artifact

Inspect the file to understand what you are dealing with.

- **Headers**: `python scripts/inspect_header.py <file>`
- **PEM Files**: If you have a `.pem` or `.key` file, extract the public key components (`n` and `e`).
  - `openssl rsa -pubin -in key.pem -text -noout`
  - `python scripts/extract_n.py <key.pem>`

### Step 2: Determine Attack Vector (RSA Focus)

Once you have `n` (modulus) and `e` (public exponent):

- **Check Key Size**: Is `n` small (< 512 bits)? -> Factorize aggressively.
- **Check `e`**: Is `e` very large? -> Possible Wiener's attack. Is `e` very small (3)? -> Cube root attack.
- **Check `n` Factors**: Run `factor_tool.py <n>` to check common databases and algorithms.

### Step 3: Execute Attack

Select the appropriate script from the toolkit:

- **Wiener's Attack**:

  ```bash
  python scripts/wiener.py --n <n_value> --e <e_value>
  ```

- **Pollard's p-1**:

  ```bash
  python scripts/pollard.py --n <n_value>
  ```

- **General Decryption**:
  If you have recovered `p` and `q` (or `d`), write a bespoke script to decrypt the ciphertext.
  - Calculate `d = inverse(e, (p-1)*(q-1))`
  - `m = pow(c, d, n)`

### Step 4: Verification

- Ensure the decrypted output makes sense (e.g., matching flag format `Detective{...}` or readable text).
- If "garbage" output, check for subsequent layers of encryption (XOR, rotation, etc.).

## Available Scripts (in ./scripts/)

- `extract_n.py`: Extracts modulus and exponent from PEM files.
- `factor_tool.py`: Interfaces with FactorDB and local algorithms to factor `n`.
- `wiener.py`: Implements Wiener's attack for small `d`.
- `pollard.py`: Implements Pollard's p-1 factorization.
- `inspect_header.py`: Dumps file headers for format analysis.
