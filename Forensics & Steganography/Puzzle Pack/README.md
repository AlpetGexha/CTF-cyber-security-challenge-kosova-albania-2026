# Puzzle Pack

Check the packets. I see a puzzle. Do you?

## Solution

The challenge involves analyzing a PCAP file (`packet_puzzle_noisy (1).pcap`) to reconstruct a hidden message split across multiple network packets.

### Analysis

1. **Traffic Analysis**: Inspecting the traffic reveals HTTP-like responses sent to sequential destination ports ranging from **12345 to 12350**.
2. **Payload Extraction**: Each relevant packet contains a JSON payload with a `fragment` field (e.g., `{"fragment": "..."}`).
3. **Reassembly**: The fragments need to be assembled in the order of their destination ports.
   - Port 12345: `bmV0d`
   - Port 12346: `29ya1`
   - Port 12347: `9mb3J`
   - Port 12348: `lbnNp`
   - Port 12349: `Y193a`
   - Port 12350: `W4=`
4. **Decoding**: Concatenating these fragments yields the Base64 string `bmV0d29ya19mb3JlbnNpY193aW4=`.
5. **Result**: Decoding the Base64 string gives the text `network_forensic_win`.

### Script

You can use the provided `script.py` to automate this process. It uses `scapy` to filter packets, extract fragments, and decode the flag.

```python
python script.py
```

### Flag

`CSC26{network_forensic_win}`
