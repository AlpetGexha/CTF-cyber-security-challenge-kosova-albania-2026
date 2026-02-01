# Scripting - Fast Fingers

## Description

The challenge requires connecting to a remote server (`mnbvcxzqwerty-csc26.cybersecuritychallenge.al:10011`) which sends a series of encrypted strings. The goal is to decrypt them using a Caesar Cipher with a specific key provided in the prompt and send back the answer within a short time limit.

## Solution

1. **Analysis**:
   - The server sends messages in the format: `Encrypted string <CIPHERTEXT> with key <SHIFT> when decrypted is:`.
   - This confirms it's a Caesar Cipher (rotation) problem.
   - The "Fast fingers won't help" hint implies we need to automate the response.

2. **Automation**:
   - Created a Python script (`script.py`) using the `socket` library.
   - **Connection**: Connects to the host and port.
   - **Loop**:
     - Receives data from the server.
     - Extracts the `ciphertext` and `shift` key using Regex.
     - Decrypts the string by shifting characters backwards by `key`.
     - Sends the result back immediately.
   - **Flag**: After successfully solving enough rounds (usually 50-100), the server returns the flag.

## Usage

Run the solver script:

```bash
python script.py
```

## Flag

`CSC26{...}` (Run script to retrieve)
