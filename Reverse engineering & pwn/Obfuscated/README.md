# Obfuscated

A corrupted script has been discovered. The JavaScript code
has been heavily obfuscated to hide the secret level access
mechanism. Your task is to deobfuscate the code to
understand the validation logic and find the correct input.

## Solution

1. **Deobfuscation**: The provided JavaScript code is heavily obfuscated. By formatting and renaming variables, we identify a main function `checkPassword(input)`.

2. **Password Analysis**: The `checkPassword` function compares the user input against a hardcoded string:

   ```javascript
   const TARGET_INPUT = "JS_HACK!";
   ```

3. **Flag Generation**: If the password matches, the script calls a function `generateFlag('js_deobfuscation_master_2024')`.

4. **Custom Hashing**: The `generateFlag` function implements a custom cryptographic hash. It relies on MD5 initial constants but uses a logic structure similar to SHA-256, albeit with "broken" or modified internal functions (e.g., simplified Sigma and Ch functions).

5. **Execution**: Extracting the deobfuscated logic into a standalone script (`script.js`) and running it generates the valid flag.

```bash
node script.js
# Output: CSC26{cacfea534920307ddd5ac8d3d3eafa2e}
```

### Flag

`CSC26{cacfea534920307ddd5ac8d3d3eafa2e}`
