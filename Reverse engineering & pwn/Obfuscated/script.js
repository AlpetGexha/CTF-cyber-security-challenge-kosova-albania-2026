// Cleaned Deobfuscated Solution
const TARGET_INPUT = "JS_HACK!";

function checkPassword(input) {
    if (input === TARGET_INPUT) {
        console.log("Access Granted!");
        // We run the hash function on the hardcoded internal string
        const flag = generateFlag('js_deobfuscation_master_2024');
        console.log("Flag: " + flag);
    } else {
        console.log("Access Denied.");
    }
}

// The custom broken-SHA function extracted from the obfuscated code
function generateFlag(input) {
    // 1. MD5 Initial Constants
    var H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476];

    // 2. Padding (Standard Merkle-Damgard)
    var msg = input;
    var originalLen = msg.length;
    msg += String.fromCharCode(0x80);
    while ((msg.length % 64) !== 56) msg += String.fromCharCode(0x00);

    // Append length (Little Endian - logic from code)
    for (var i = 0; i < 8; i++) {
        msg += String.fromCharCode((originalLen * 8) >>> (i * 8) & 0xFF);
    }

    // 3. Processing Blocks
    // SHA-256 K-Constants
    var K = [
        0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
        0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
        0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
        0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
        0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
        0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
        0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
        0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
    ];

    for (var offset = 0; offset < msg.length; offset += 64) {
        var W = [];
        for (var i = 0; i < 16; i++) {
            W[i] = (msg.charCodeAt(offset + i * 4) << 24) |
                (msg.charCodeAt(offset + i * 4 + 1) << 16) |
                (msg.charCodeAt(offset + i * 4 + 2) << 8) |
                (msg.charCodeAt(offset + i * 4 + 3));
        }
        for (var i = 16; i < 64; i++) {
            var w2 = W[i - 2];
            var w15 = W[i - 15];
            // SHA-256 Schedule logic (Standard)
            var s1 = ((w2 >>> 17) | (w2 << 15)) ^ ((w2 >>> 19) | (w2 << 13)) ^ (w2 >>> 10);
            var s0 = ((w15 >>> 7) | (w15 << 25)) ^ ((w15 >>> 18) | (w15 << 14)) ^ (w15 >>> 3);
            W[i] = (s1 + W[i - 7] + s0 + W[i - 16]) | 0;
        }

        var work = H.slice(); // Copy A,B,C,D. Length is 4.

        for (var i = 0; i < 64; i++) {
            // "Broken" Sigma0: Only uses Rotate Right 2
            var S0 = (work[0] >>> 2) | (work[0] << 30);

            // "Broken" Ch: XORs A, B, C
            var ch = work[0] ^ work[1] ^ work[2];

            // Temp1
            // Note: work[3] is defined. K[i], W[i] are defined.
            var t1 = (work[3] + S0 + ch + K[i] + W[i]) | 0;

            // "Broken" Sigma1: Only uses Rotate Right 6 on index 4 (E)
            // Note: work[4] is undefined in first iteration! (treated as 0)
            var e_val = work[4] | 0;
            var S1 = (e_val >>> 6) | (e_val << 26);

            // "Broken" Maj: XORs E, F, G (indices 4,5,6)
            var maj = (work[4] | 0) ^ (work[5] | 0) ^ (work[6] | 0);

            var t2 = (t1 + S1 + maj) | 0;

            // Weird Update Order
            work[3] = work[2];
            work[2] = work[1];
            work[1] = work[0];
            work[0] = t2;
            work[7] = work[6];
            work[6] = work[5];
            work[5] = work[4];
            // New E is calculated as Old D + New A
            work[4] = (work[3] + t2) | 0;
        }

        for (var i = 0; i < 4; i++) H[i] = (H[i] + work[i]) | 0;
    }

    var hex = '';
    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            hex += ((H[i] >>> (24 - j * 8)) & 0xFF).toString(16).padStart(2, '0');
        }
    }
    return 'CSC26{' + hex + '}';
}

// Run the check
checkPassword("JS_HACK!");