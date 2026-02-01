# How to Retrieve the Flag

Based on the challenge description and your intuition, this is an **SSRF (Server-Side Request Forgery)** challenge that likely uses a validator to check if the URL points to a private IP (like 127.0.0.1) before visiting it.

You are correct: The "pretend to be Google, then switch to localhost" technique is called **DNS Rebinding**.

## Strategy 1: DNS Rebinding (Recommended)

This attack works by exploiting the time difference between when the server _checks_ the URL and when it _visits_ it (TOCTOU - Time of Check, Time of Use).

1.  **Open the Tool**: Go to [https://lock.cmpxchg8b.com/rebinder.html](https://lock.cmpxchg8b.com/rebinder.html).
2.  **Configure IPs**:
    - **A (Safe IP)**: Enter a public, safe IP address. You can use Google's DNS `8.8.8.8` or a web server you control.
    - **B (Target IP)**: Enter `127.0.0.1` (Localhost).
3.  **Get the Domain**: Detailed instructions are on the site, but it will give you a domain like `7f000001.08080808.rbndr.us`.
4.  **Attack**:
    - Paste this domain into the **Analyzer** on the challenge website.
    - The Analyzer will resolve the domain.
      - _First check_: It might see `8.8.8.8` (Safe).
      - _Second fetch_: It might see `127.0.0.1` (Target).
    - If it fails, **try again multiple times**. DNS Rebinding often requires luck/persistence because of browser/OS caching.

## Strategy 2: URL Bypasses (Try these first)

Before doing complex rebinding, try these simple bypasses in the Analyzer input. I have saved these to `payload` file for you.

- `http://127.1` (Shortened localhost)
- `http://2130706433` (Decimal version of 127.0.0.1)
- `http://0x7f000001` (Hex version)
- `http://0/`
- `http://localtest.me` (A public domain that always resolves to 127.0.0.1)

## Strategy 3: HTTP Redirect

"Ti boje kishe o tu hi ngoogle edhe aj menon qe n'google Edue e bon redirect shembull te local hosti"

This describes an Open Redirect attack. If the Analyzer follows redirects:

1.  You need a server you control (or a service).
2.  Create a script (e.g., PHP/Python) that sends a `Location: http://127.0.0.1` header.
3.  Give the Analyzer your server's URL. It visits you (safe), then you tell it to go to `localhost`.

If you don't have a server, you can use a service or try the DNS Rebinding method which acts similarly but at the network layer.

## Search Terms

If you need to research more:

- "SSRF DNS Rebinding CTF"
- "SSRF bypass list"
- "Tavis Ormandy DNS Rebinding"
