---
name: Mobile & Android Security Specialist
description: A specialized skill for analyzing Android applications (APK), reverse engineering Dalvik bytecode, and exploiting mobile vulnerabilities.
---

# Mobile Security Specialist Skill

This skill analyzes Android package files (APK) to find hardcoded secrets, analyze logic in Dalvik/Smali, and exploit Intent vulnerabilities.

## Capabilities

1.  **Decompilation & Static Analysis**
    - **JADX**: Converting APKs to Java source code for logic analysis.
    - **APKTool**: Decoded resources and `AndroidManifest.xml`.
    - **Smali**: Reading lower-level Dalvik assembly if decompilation fails.

2.  **Manifest Analysis**
    - **Permissions**: Checking for dangerous permissions (READ_SMS, EXTERNAL_STORAGE).
    - **Components**: Identifying exported Activities, Services, and Broadcast Receivers.
    - **Intents**: Understanding input filters (Action, Category, Data) for logic flaws.

3.  **Data Storage Analysis**
    - **SharedPreferences**: Checking XML files for plaintext credentials.
    - **SQLite Databases**: Inspecting local `.db` files.
    - **Strings.xml**: Looking for API keys or secrets in resource files.

## Workflow

### Step 1: Unpacking & Decompilation

- **Manifest View**: Use `jadx <file.apk>` to view the `AndroidManifest.xml` first.
  - Look for `android:exported="true"`.
- **Source Review**: Browse the package structure (e.g., `com.example.challenge`).
  - Check `MainActivity` for entry logic.
  - Check `strings.xml` in `res/values/`.

### Step 2: Code Analysis (Java)

- Search for keywords: `Flag`, `Password`, `Secret`, `AES`, `Base64`.
- Trace the input: If a text box accepts a flag, follow the `onClick` listener to the verification function.
- **Native Libraries**: If you see `System.loadLibrary("foo")`, the logic is in a `.so` file (requires `Reverse Engineering` skill).

### Step 3: Patching & Dynamic (Advanced)

- If static analysis is blocked (obfuscation), you may need to patch smali code.
- Use `apktool d` -> Edit `.smali` -> `apktool b` -> Sign.

## Tool Reference

- `jadx`: Java Decompiler.
- `apktool`: Resource decoder.
- `adb`: Android Debug Bridge (connecting to emulators).
