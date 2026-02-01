encoded = """
Charlie Sierra Charlie 2 6 {Alfa Charlie Bravo Foxtrot Echo Echo Echo
Golf Golf Delta Golf Alfa Golf Oscar Lima Alfa Charlie Bravo Oscar
Echo Alfa Charlie Tango Yankee Golf Foxtrot Lima Echo Kilo Oscar Lima
Echo Echo Echo Papa Papa Charlie Lima Sierra }
"""

decoded = ""

for word in encoded.split():
    prefix = ""
    suffix = ""

    # keep leading non-letters (like '{')
    while word and not word[0].isalpha():
        prefix += word[0]
        word = word[1:]

    # keep trailing non-letters (like '}')
    while word and not word[-1].isalpha():
        suffix = word[-1] + suffix
        word = word[:-1]

    if word:
        decoded += prefix + word[0] + suffix
    else:
        decoded += prefix + suffix

print(decoded)
