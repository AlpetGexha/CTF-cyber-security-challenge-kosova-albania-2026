from scapy.all import rdpcap, TCP, Raw

PCAP_FILE = "What_is_encrypti0n (1).pcapng"
MODBUS_PORT = 502
READ_HOLDING_REGISTERS = 0x03


def is_modbus_packet(pkt):
    """Check if packet is Modbus/TCP (port 502)."""
    return TCP in pkt and (pkt[TCP].sport == MODBUS_PORT or pkt[TCP].dport == MODBUS_PORT)


def parse_read_request(pkt):
    """
    Parse Modbus Read Holding Registers request.
    Returns (start_address, quantity) or None.
    """
    if Raw not in pkt:
        return None

    data = pkt[Raw].load

    # Minimum length for MBAP + function + address + quantity
    if pkt[TCP].dport != MODBUS_PORT or len(data) < 12:
        return None

    func_code = data[7]
    if func_code != READ_HOLDING_REGISTERS:
        return None

    start_addr = (data[8] << 8) | data[9]
    quantity = (data[10] << 8) | data[11]

    return start_addr, quantity


def parse_read_response(pkt):
    """
    Parse Modbus Read Holding Registers response.
    Returns list of register values.
    """
    if Raw not in pkt or pkt[TCP].sport != MODBUS_PORT:
        return []

    data = pkt[Raw].load
    if len(data) < 9 or data[7] != READ_HOLDING_REGISTERS:
        return []

    byte_count = data[8]
    values = []

    for i in range(9, 9 + byte_count, 2):
        if i + 1 < len(data):
            value = (data[i] << 8) | data[i + 1]
            values.append(value)

    return values


def printable_char(value):
    """Return ASCII character if printable, else '?'."""
    return chr(value) if 32 <= value < 127 else "?"


def main():
    packets = rdpcap(PCAP_FILE)

    modbus_packets = [p for p in packets if is_modbus_packet(p)]
    print(f"Total Modbus packets: {len(modbus_packets)}")

    register_data = []

    # Assume request/response pairs
    for i in range(0, len(modbus_packets) - 1, 2):
        request = modbus_packets[i]
        response = modbus_packets[i + 1]

        req_info = parse_read_request(request)
        if not req_info:
            continue

        start_addr, quantity = req_info
        values = parse_read_response(response)

        for offset, value in enumerate(values):
            register_data.append({
                "address": start_addr + offset,
                "value": value
            })

    print(f"\nExtracted {len(register_data)} register reads:")
    for idx, item in enumerate(register_data):
        addr = item["address"]
        val = item["value"]

        print(
            f"{idx}: "
            f"Register {addr} (0x{addr:04x}) = "
            f"{val} (0x{val:04x}) | "
            f"addr='{printable_char(addr)}' "
            f"val='{printable_char(val & 0xFF)}'"
        )

    print("\n--- Attempt: Register addresses as ASCII ---")
    addresses = [item["address"] for item in register_data]
    ascii_view = "".join(printable_char(a) for a in addresses)

    print(f"Addresses: {addresses}")
    print(f"As ASCII: {ascii_view}")


if __name__ == "__main__":
    main()
