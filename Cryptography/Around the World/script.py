import re
import os

# Coordinate to City Name mapping
# Derived from the coordinates provided in the challenge
COORD_MAP = {
    (42.6629, 21.1655): "Pristina",
    (37.9838, 23.7275): "Athens",
    (-33.8688, 151.2093): "Sydney",
    (48.8566, 2.3522): "Paris",
    (59.9139, 10.7522): "Oslo",
    (41.9028, 12.4964): "Rome",
    (35.6895, 139.6917): "Tokyo",
    (43.6532, -79.3832): "Toronto",
    (43.7696, 11.2558): "Florence",
    (51.5074, -0.1278): "London",
    (52.3676, 4.9041): "Amsterdam",
    (23.1291, 113.2644): "Guangzhou",
    (1.3521, 103.8198): "Singapore",
}

def get_city_initial(lat, lon):
    # Find the closest match in our map with a small tolerance
    # This handles potential floating point parsing differences
    for (target_lat, target_lon), city in COORD_MAP.items():
        if abs(lat - target_lat) < 0.001 and abs(lon - target_lon) < 0.001:
            return city[0].upper()
    return '?'

def decrypt():
    file_path = os.path.join(os.path.dirname(__file__), 'encrypted_message.txt')
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}")
        return

    print(f"Encrypted content: {content}")

    # Extract the parts inside the braces CSC26{...}
    match = re.search(r'CSC26\{(.*)\}', content)
    if not match:
        print("Could not find flag format CSC26{...}")
        # Try processing the whole string if braces are missing, or just fail
        return

    inner_content = match.group(1)
    
    # Split by underscore which seems to separate words
    words_raw = inner_content.split('_')
    
    decoded_words = []
    
    for word_raw in words_raw:
        # Find all coordinate pairs (lat, lon)
        # Regex captures two groups: lat and lon
        pairs = re.findall(r'\((-?[\d\.]+),\s*(-?[\d\.]+)\)', word_raw)
        
        current_word = ""
        for lat_str, lon_str in pairs:
            lat = float(lat_str)
            lon = float(lon_str)
            initial = get_city_initial(lat, lon)
            current_word += initial
            
        decoded_words.append(current_word)
        
    final_string = "_".join(decoded_words)
    flag = f"CSC26{{{final_string}}}"
    
    print("\nDecryption Result:")
    print(f"Decoded words: {decoded_words}")
    print(f"Final Flag: {flag}")

if __name__ == "__main__":
    decrypt()
