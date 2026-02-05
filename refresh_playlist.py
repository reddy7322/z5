import requests
import json
import re

# URLs from your provided sources
M3U_URL = "https://raw.githubusercontent.com/cloudplay97/m3u/refs/heads/main/zee/zee5.m3u"
LOGO_JSON_URL = "https://tvtelugu.pages.dev/logo/channels.json"

def fetch_data():
    # Fetch M3U and JSON
    m3u_content = requests.get(M3U_URL).text
    logos_data = requests.get(LOGO_JSON_URL).json()
    
    # Create a lookup dictionary for logos
    logo_lookup = {item['Channel Name'].lower(): item['logo'] for item in logos_data}
    
    # Simple logic to update logos if names match
    lines = m3u_content.splitlines()
    updated_lines = []
    
    for line in lines:
        if line.startswith("#EXTINF"):
            # Extract channel name from the end of the line
            channel_name = line.split(',')[-1].strip().lower()
            if channel_name in logo_lookup:
                # Update the tvg-logo attribute using regex
                new_logo = logo_lookup[channel_name]
                line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{new_logo}"', line)
        updated_lines.append(line)
    
    # Save the updated playlist
    with open("updated_zee5.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(updated_lines))
    print("Playlist updated successfully.")

if __name__ == "__main__":
    fetch_data()
