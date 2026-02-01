# The Pirate's Hidden Vault

Legend says the caves of Haxhi Alia were a sanctuary for
pirates and heroes. Now, Detective The Pixel has chosen this
historic hideout as their final vault. Your mission is to breach
this digital sanctuary, The Pixel's secret, a flag in the format
CSC26{ ... } which is concealed with an unknown encoding.

## Architecture

The image `stego_image.png` contains a hidden LSB steganography message in the RGB channels.
The extracted bits form a Base32 encoded string.
Decoding the Base32 string reveals the flag.

## Steps

1. Used Python to extract LSBs from R, G, B channels of each pixel.
2. Filtered the resulting data for valid Base32 characters ending with `======`.
3. Decoded the Base32 string.

Run the script `script.py` to extract the flag.

INJUGMRWPMYGGMBQGZSGKNBSGY4DANRTHAYTGNJYGE4DOYLGMNSGGNTEMRSTKZLEGIZTQNJZMEYWCZJWMMYTAM3BMZQTCMZYMZRWMOBWHAZTAMLCPU======

## Final Flag

`CSC26{0c006de426806381358187afcdc6dde5ed23859a1ae6c103afa138fcf868301b}`
