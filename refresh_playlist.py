import requests
import re

M3U_URL = "https://raw.githubusercontent.com/cloudplay97/m3u/refs/heads/main/zee/zee5.m3u"
LOGO_JSON_URL = "https://tvtelugu.pages.dev/logo/channels.json"

def fetch_and_modify():
    # 1. Fetch Data
    m3u_response = requests.get(M3U_URL).text
    logos_data = requests.get(LOGO_JSON_URL).json()
    
    # Create a clean logo map: {"zeetv": "url"}
    logo_map = {item['Channel Name'].replace(" ", "").lower(): item['logo'] for item in logos_data}
    
    # IDs to move to the "𝐓𝐞𝐥𝐮𝐠𝐮" group
    telugu_ids = ["0-9-zeecinemalu", "0-9-zeetelugu", "0-9-9z5383485", "0-9-9z5383488"]
    
    lines = m3u_response.splitlines()
    final_output = ["#EXTM3U"] # Start fresh with only the M3U tag
    
    for line in lines:
        # Skip the original headers you wanted removed
        if line.startswith("# Pushed") or line.startswith("# Telegram") or line.startswith("#EXTM3U"):
            continue
            
        if line.startswith("#EXTINF"):
            # 1. Update Group for specific IDs
            for t_id in telugu_ids:
                if f'tvg-id="{t_id}"' in line:
                    line = re.sub(r'group-title="[^"]*"', 'group-title="𝐓𝐞𝐥𝐮𝐠𝐮"', line)
            
            # 2. Extract Name and Match Logo
            # Looks for name after the last comma
            name_part = line.split(',')[-1].strip()
            # Clean name for matching (remove spaces and "HD")
            clean_name = name_part.lower().replace(" ", "").replace("hd", "")
            
            if clean_name in logo_map:
                new_logo = logo_map[clean_name]
                line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{new_logo}"', line)
                    
        final_output.append(line)

    # Save processed file
    with open("updated_zee5.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
    print("M3U Updated: Headers removed, Logos synced, and Groups assigned.")

if __name__ == "__main__":
    fetch_and_modify()
