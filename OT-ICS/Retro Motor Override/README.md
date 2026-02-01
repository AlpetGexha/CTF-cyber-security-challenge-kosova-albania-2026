# Retro Motor Override

A Programmable Logic Controller (PLC) is used to control some motors of a Nuclear Plant. The communication between the PLC and the motor actuators is done by the Modbus Protocol. Use this protocol's vulnerabilities to increase the speed of one of the motors

https://retromotoroverride-csc26.cybersecuritychallenge.al/ nc motoroverride-csc26.cybersecuritychallenge.al 502

## Solution

1. **Analysis**: The challenge involves a PLC communicating via Modbus TCP. We are given an endpoint to connect to.
2. **Modbus Interaction**:
   - The goal is to override the motor speed.
   - Using a Modbus client (like `pymodbus` or `mbpoll`), we connect to port 502.
   - We identify Coil 0 controls "Auto Mode". We disable it by writing `False` (0).
   - We identify Register 0 (and possibly 1) controls the speed. We write a high value, e.g., `4200`.
3. **Execution**:
   - Run the provided `script.py` which automates these Modbus commands.
   - The script then checks the web dashboard (`/flag` endpoint) to retrieve the flag.

```bash
python script.py
```

### Flag

`CSC26{Y0u_C0rrUp7eD_Th3_C0r3!}`
