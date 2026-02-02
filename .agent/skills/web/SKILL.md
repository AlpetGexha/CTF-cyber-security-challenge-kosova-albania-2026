---
name: Web Exploitation Specialist
description: A specialized skill for analyzing web applications, identifying vulnerabilities (SSRF, SQLi, XSS), and automating exploitation.
---

# Web Exploitation Specialist Skill

This skill equips the agent with the ability to perform reconnaissance, vulnerability assessment, and exploitation of web applications.

## Capabilities

1.  **Reconnaissance & Enumeration**
    - **Source Code Review**: Analyze HTML/JS for comments, hidden inputs, and API endpoints.
    - **Endpoint Fuzzing**: Identify hidden files (robots.txt, .git/, backup files, .DS_Store) and directories.
    - **Header Analysis**: Inspect HTTP headers for server info, cookies, and security policies (CSP).

2.  **Vulnerability Identification**
    - **SSRF (Server-Side Request Forgery)**: Testing input fields that accept URLs (webhooks, image loaders) to access internal resources (localhost, metadata services).
    - **SQL Injection**: Testing login forms and URL parameters with common payloads (`' OR 1=1 --`, `UNION SELECT`).
    - **GraphQL Injection**: Introspection queries (`{__schema{types{name fields{name}}}}`) to leak schema and find hidden mutations/queries.
    - **IDOR**: Manipulating IDs in URLs/requests to access unauthorized data.
    - **CSRF/XSS**: Checking for reflected input script tags.
    - **JWT Attacks**: Checking for `None` algorithm, weak secrets, or information leakage in the payload.

3.  **Exploitation & Automation**
    - **Python Requests**: Using the `requests` library to automate form submissions, session management, and brute-forcing.
    - **Response Analysis**: Parsing HTML responses (BeautifulSoup, Regex) to extract flags or tokens.

## Workflow

### Step 1: Initial Recon

- Open the target URL.
- Check `robots.txt`, `sitemap.xml`.
- **GraphQL Check**: Try appending `/graphql`, `/api/graphql`, `/v1/graphql` to the URL.
- View Page Source (`Ctrl+U` equivalent). Look for comments `<!-- -->`.

### Step 2: Input Vector Analysis

- Identify all user input points: Forms, URL parameters, Cookie values, HTTP Headers.
- Test simple payloads to see how the application reacts.

### Step 3: Scripted Interaction

Use the templates in `./scripts/` to automate interaction when manual testing is too slow or complex.

- **Generic Solver Template**: `python scripts/generic_solver_template.py`
  - Modify this script to handle session creation and POST requests.
- **Payload Fuzzing**: `python scripts/debug_payloads.py`
  - Use this to iterate through a list of payloads against a specific target parameter.

### Step 4: Special Cases

- **SSRF**:
  - Try `http://127.0.0.1`, `http://localhost`, `0.0.0.0`.
  - Try specialized payloads (gopher://, dict://).
- **GraphQL**:
  - If found, run an Introspection Query to map the _entire_ API.
  - Look for fields like `private`, `flag`, `userPassword`.

## Available Scripts (in ./scripts/)

- `generic_solver_template.py`: A basic structure for a CTF solve script using `requests`.
- `debug_payloads.py`: A script to iterate through a list of payloads and check responses.
- `analyze_response.py`: Utilities for search text patterns (flags) in HTTP responses.
