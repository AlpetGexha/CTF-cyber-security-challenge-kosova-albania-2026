# What is encrypti0n

Does Modbus know what encryption is? And who is it
referring to?

## Solution

1. **Analysis**: The challenge provides a PCAP file (`What_is_encrypti0n (1).pcapng`) containing network traffic.
2. **Protocol Inspection**: Opening the file in Wireshark reveals **Modbus/TCP** traffic.
3. **Vulnerability**: Modbus is an unencrypted, cleartext protocol.
4. **Flag Extraction**: By inspecting the packet payloads (specifically `Write Multiple Registers` or response packets), we can see ASCII data.
   - Following the TCP stream or inspecting the packet details reveals the flag directly in the payload.

### Flag

`CSC{M0d2u5_NoT_3ncrY9t#d}`
