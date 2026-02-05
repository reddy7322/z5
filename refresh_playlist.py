import requests
import re

M3U_URL = "https://raw.githubusercontent.com/cloudplay97/m3u/refs/heads/main/zee/zee5.m3u"
LOGO_JSON_URL = "https://tvtelugu.pages.dev/logo/channels.json"

def fetch_and_modify():
    # 1. Fetch Data
    m3u_content = requests.get(M3U_URL).text
    logos_data = requests.get(LOGO_JSON_URL).json()
    
    # Create logo mapping: {"Channel Name": "URL"}
    logo_map = {item['Channel Name'].lower(): item['logo'] for item in logos_data}
    
    # List of IDs to move to the "𝐓𝐞𝐥𝐮𝐠𝐮" group
    telugu_ids = ["0-9-zeecinemalu", "0-9-zeetelugu", "0-9-9z5383485", "0-9-9z5383488"]
    
    lines = m3u_content.splitlines()
    final_output = []
    
    for line in lines:
        if line.startswith("#EXTINF"):
            # Update Logo based on Channel Name (JSON Match)
            channel_name_match = re.search(r',(.+)$', line)
            if channel_name_match:
                name = channel_name_match.group(1).strip().lower()
                if name in logo_map:
                    line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{logo_map[name]}"', line)
            
            # Update Group to "𝐓𝐞𝐥𝐮𝐠𝐮" if tvg-id matches your list
            for t_id in telugu_ids:
                if f'tvg-id="{t_id}"' in line:
                    line = re.sub(r'group-title="[^"]*"', 'group-title="𝐓𝐞𝐥𝐮𝐠𝐮"', line)
                    break
                    
        final_output.append(line)

    # Save processed file
    with open("updated_zee5.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
    print("M3U Updated: Logos matched and Telugu groups assigned.")

if __name__ == "__main__":
    fetch_and_modify()
