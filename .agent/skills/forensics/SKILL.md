---
name: Forensics & Steganography Specialist
description: A specialized skill for analyzing file artifacts, extracting hidden data, and solving steganography challenges.
---

# Forensics & Steganography Specialist Skill

This skill focuses on dissecting files to find hidden information, whether it's embedded data, metadata, or steganographic encoding.

## Capabilities

1.  **File Identification & Extraction**
    - **Magic Bytes**: Identifying files by their hex signature (e.g., `FF D8 FF` for JPG, `50 4B 03 04` for ZIP).
    - **Binwalk**: extracting embedded files and firmware images.
    - **Strings**: Extracting readable text from binary blobs.

2.  **Metadata Analysis**
    - **Exiftool**: Checking images and documents for authors, comments, GPS data, or hidden flags.
    - **File System Artifacts**: Analyzing timestamps and permissions.

3.  **Image Analysis & Repair**
    - **Header Repair**: Fixing corrupted magic bytes (e.g., fixing a PNG header to make it viewable).
    - **LSB (Least Significant Bit)**: Detecting messages hidden in the lowest bits.
    - **Visual Analysis**: Adjusting brightness/contrast/planes (StegSolve).

4.  **Audio/Video Steganography**
    - **Spectrograms**: Visualizing audio frequencies (often hides text).
    - **DTMF**: Decoding phone dial tones.
    - **Deep Sound**: Checking for hidden files in WAV/MP3.

## Workflow

### Step 1: Surface Analysis

- **Run `file <filename>`**: Determine the true file type.
- **Run `strings <filename> | grep "flag"`**: Look for low-hanging fruit.
- **Run `exiftool <filename>`**: Check for metadata hints.

### Step 2: Deep Dive

- **Header Check**: Open in Hex Editor. Does it match the file extension?
  - PNG: `89 50 4E 47 0D 0A 1A 0A`
  - JPG: `FF D8 FF`
  - If not, **Edit and Repair**.
- **Binwalk**: `binwalk -e <filename>` to extract hidden contents.

### Step 3: Steganography Specifics

- **Images**: Use `zsteg` (PNG) or `steghide` (JPG).
- **Audio**: Open in Audacity. switch view to "Spectrogram". Look for visual text.

### Step 4: Custom Decoding (Python)

If tools fail, the data is likely encoded with a custom scheme.

- **Image manipulation**: Use `PIL` (Pillow) to access pixel data.
  ```python
  from PIL import Image
  img = Image.open('challenge.png')
  pixels = img.load()
  # Iterate over x, y to analyze r, g, b values
  ```

## Tool Reference

- `binwalk`: Firmware/file extraction.
- `foremost`: File craving.
- `zsteg`: PNG/BMP steganography detection.
- `steghide`: JPG/WAV embedding tool.
