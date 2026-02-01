#!/usr/bin/env python3

from scapy.all import *
import base64

def solve_puzzle():
    # Load the pcap file
    print("[*] Loading pcap file...")
    pkts = rdpcap('packet_puzzle_noisy (1).pcap')
    print(f"[+] Loaded {len(pkts)} packets")
    
    # Filter for HTTP responses (port 80) to sequential ports 12345-12350
    print("\n[*] Searching for puzzle pieces...")
    target_ports = range(12345, 12351)
    
    puzzle_pieces = []
    for pkt in pkts:
        if TCP in pkt and pkt[TCP].sport == 80 and pkt[TCP].dport in target_ports and Raw in pkt:
            dport = pkt[TCP].dport
            payload = bytes(pkt[Raw].load).decode('utf-8', errors='ignore')
            
            # Extract JSON fragment
            if '"fragment":"' in payload:
                start = payload.find('"fragment":"') + len('"fragment":"')
                end = payload.find('"', start)
                fragment = payload[start:end]
                puzzle_pieces.append((dport, fragment))
                print(f"[+] Found fragment at port {dport}: {fragment}")
    
    # Sort by port number to get correct order
    puzzle_pieces.sort(key=lambda x: x[0])
    
    # Combine fragments
    print("\n[*] Combining fragments...")
    combined = ''.join([piece[1] for piece in puzzle_pieces])
    print(f"[+] Combined Base64: {combined}")
    
    # Decode Base64
    print("\n[*] Decoding Base64...")
    flag = base64.b64decode(combined).decode('utf-8')
    
    print("\n" + "="*60)
    print(f"[!] FLAG FOUND: {flag}")
    print(f"CSC26{{{flag}}}")
    print("="*60)
    
    return flag

if __name__ == "__main__":
    solve_puzzle()
