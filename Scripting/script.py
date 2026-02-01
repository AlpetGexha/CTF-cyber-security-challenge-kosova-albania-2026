#!/usr/bin/env python3
# CTF Caesar Cipher Solver

import socket
import re
import sys

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            result += decrypted_char
        else:
            result += char
    return result

HOST = "mnbvcxzqwerty-csc26.cybersecuritychallenge.al"
PORT = 10011

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("Connected to server!", flush=True)
round_count = 0

try:
    s.settimeout(2)
    data_buffer = ""
    
    while True:
        try:
            chunk = s.recv(1024).decode('utf-8', errors='ignore')
            if not chunk:
                print("Connection closed", flush=True)
                break
                
            data_buffer += chunk
            print(f"Buffer: {repr(data_buffer)}", flush=True)
            
            # Check for flag pattern
            if "CSC26{" in data_buffer or "flag{" in data_buffer.lower():
                print(f"\n🚩 FLAG FOUND!\n{data_buffer}", flush=True)
                break
            
            # Look for the challenge pattern
            match = re.search(r'Encrypted string (\S+) with key (\d+) when decrypted is:', data_buffer)
            if match:
                encrypted = match.group(1)
                key = int(match.group(2))
                
                decrypted = caesar_decrypt(encrypted, key)
                round_count += 1
                print(f"Round {round_count}: {encrypted} (shift={key}) -> {decrypted}", flush=True)
                
                # Send answer immediately
                s.sendall((decrypted + "\n").encode())
                
                # Clear buffer after this challenge
                data_buffer = ""
                
        except socket.timeout:
            continue
        except Exception as e:
            print(f"Error in loop: {e}", flush=True)
            break
            
except KeyboardInterrupt:
    print("\nInterrupted by user", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)
finally:
    s.close()
    print("Connection closed", flush=True)
