---
name: Reverse Engineering & Pwn Specialist
description: A specialized skill for analyzing binaries, decompiling code, and exploiting memory corruption vulnerabilities.
---

# Reverse Engineering & Pwn Specialist Skill

This skill enables the agent to disassemble, decompile, debug, and exploit binary applications (ELF/PE).

## Capabilities

1.  **Static Analysis**
    - **Disassembly**: Reading x86/x64/ARM assembly using `objdump -d` or `ghidra` analysis.
    - **File Info**: Using `checksec` (to see NX, Canary, PIE), `file`, and `readelf`.
    - **Strings**: Finding hardcoded passwords or prompts.

2.  **Dynamic Analysis**
    - **GDB**: Debugging execution, setting breakpoints, inspecting registers (`info registers`) and memory (`x/10wx $esp`).
    - **Tracing**: using `ltrace` (library calls) and `strace` (system calls) to understand program flow without full debugging.

3.  **Vulnerability Classes (Pwn)**
    - **Buffer Overflow**: Overwriting return addresses to control execution flow (ret2win, ROP).
    - **Format String**: Leaking memory or writing to arbitrary addresses using `%x` and `%n`.
    - **Integer Overflow**: Causing unexpected wrapping to bypass checks.

## Workflow

### Step 1: Triage

- `file <binary>`: Architecture (32/64 bit), stripped/not stripped.
- `checksec --file=<binary>`: Protections (Stack Canary, NX, PIE, RELRO).
- `strings <binary>`: Quick check for flags.

### Step 2: Static Analysis

- Analyze control flow. Look at the `main` function.
- Identify "win" functions (e.g., `print_flag`).
- Identify dangerous functions (`gets`, `strcpy`, `scanf`, `printf(user_input)`).

### Step 3: Dynamic Analysis

- Run the program normally to understand inputs.
- Run with `ltrace` to see comparison values (`strcmp`).
- Crash the program (large input) to test for overflows.
  - Find the offset to the crash (cyclic patterns).

### Step 4: Exploitation

- Construct a payload script using Python.

  ```python
  import struct
  import socket

  # 64-bit packing
  p64 = lambda x: struct.pack('<Q', x)

  offset = 40
  target_addr = 0x401135

  payload = b'A' * offset + p64(target_addr)
  print(payload)
  ```

## Tool Reference

- `gdb`: The GNU Debugger.
- `objdump`: Linear disassembly.
- `ltrace`/`strace`: Tracing tools.
- `readelf`: ELF format analysis.
