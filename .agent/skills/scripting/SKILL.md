---
name: Automation & Scripting Specialist
description: A specialized skill for rapid prototyping, data parsing, brute-forcing, and automating repetitive tasks in CTFs.
---

# Automation & Scripting Specialist Skill

This skill allows the agent to quickly generate scripts to solve logical challenges, parse massive datasets, or automate interactions.

## Capabilities

1.  **Data Parsing & text Processing**
    - **Regex**: complex pattern matching for flag extraction.
    - **Format Conversion**: Binary <-> Hex <-> Base64 <-> ASCII conversions using python `biascii` / `base64`.
    - **File Handling**: Reading/Writing large files efficiently.

2.  **Brute-Force & Iteration**
    - **Itertools**: Generating permutations and combinations.
    - **Wordlists**: Iterating through dictionary files.
    - **Parallelism**: using `threading` or `multiprocessing` for speed.

3.  **Network Interaction**
    - **Sockets**: Raw TCP/UDP connections for non-HTTP challenges (Cipher Sprints).
    - **Requests**: HTTP/HTTPS automation.

## Workflow

### Step 1: Input Analysis

- Determine the format of the data (space separated, CSV, JSON, raw binary).
- Identify the goal (find a specific string, sum numbers, crack a hash).

### Step 2: Prototyping

- Write a quick Python script.
- Start small (test on the first 10 lines/items).
- Verify logic before running on the full dataset.

### Step 3: Scaling

- If the task is slow, optimize.
  - Use `set()` for lookups instead of `list()`.
  - Use `mmap` for massive files.

## Useful Scripts (in ./scripts/)

- `socket_solver_template.py`: A template for connecting to a server, receiving data, processing it, and sending the answer back in a loop.

## Common Snippets

**Socket Interaction**:

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('target.com', 1337))
# Read until a prompt
buffer = ""
while "Answer:" not in buffer:
    data = s.recv(1024).decode()
    buffer += data
s.send(b'answer\n')
```
