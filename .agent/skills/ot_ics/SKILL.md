---
name: OT-ICS Security Specialist
description: A specialized skill for analyzing industrial control systems, protocols (Modbus, DNP3), and recovering data from OT network captures.
---

# OT-ICS Security Specialist Skill

This skill analyzes Operational Technology (OT) and Industrial Control Systems (ICS) challenges, focusing on proprietary protocols and legacy hardware emulations.

## Capabilities

1.  **Protocol Analysis**
    - **Modbus/TCP**: Analyzing Function Codes (Read Coils, Write Register), Unit IDs, and register values.
    - **DNP3**: Analyzing Master/Outstation communication.
    - **S7 Comm**: Siemens specific protocol analysis.

2.  **Traffic Analysis (PCAP)**
    - Filtering industrial traffic in Wireshark/TShark.
    - Extracting payloads from command packets.
    - Identifying anomalous setpoints or commands (e.g., "Stop Motor").

3.  **Simulation & Interaction**
    - Using Python (`pymodbus`) to interact with simulated PLCs.
    - Querying registers to find flags hidden in memory maps.

## Workflow

### Step 1: Protocol Identification

- Analyze PCAP headers or port numbers (502 for Modbus, 20000 for DNP3).
- Identify the Master (Controller) and Slave (Device) IPs.

### Step 2: Traffic Dissection

- **Modbus**: Look for specific Function Codes:
  - `1` (Read Coils) / `5` (Write Single Coil).
  - `3` (Read Holding Registers) / `6` (Write Single Register).
  - `16` (Write Multiple Registers) -> often used to upload data/flags.
- **Values**: Convert register values (16-bit integers) to ASCII.

### Step 3: Interaction (Active Challenges)

- If a target IP:Port is given, scan it.
- Use `pymodbus` to dump all registers.
  ```python
  from pymodbus.client import ModbusTcpClient
  client = ModbusTcpClient('target_ip')
  result = client.read_holding_registers(0, 100)
  print(result.registers)
  ```

## Tool Reference

- `Wireshark`/`tshark`: Traffic analysis.
- `pymodbus`: Python library for Modbus interaction.
- `scapy`: Packet manipulation.
