import re
import json

# Load the schemes text file
file_path = "C:\SIH_BACKEND\External_data\scheme_news\output2\schemes.txt"
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# Regex to extract scheme details
pattern = re.compile(
    r"SCHEME NAME:\s*(.*?)\n\nSCHEME DETAILS:\n(.*?)(?:\n\nKEYWORDS:\s*(.*?)\n\n=+|$)",
    re.S
)

schemes = []
for match in pattern.findall(text):
    name, details, keywords = match
    scheme_data = {
        "scheme_name": name.strip(),
        "scheme_details": details.strip(),
        "keywords": [k.strip() for k in keywords.split(",")] if keywords else []
    }
    schemes.append(scheme_data)

# Save JSON output
output_path = "C:\SIH_BACKEND\External_data\scheme_news\schemes.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(schemes, f, indent=4, ensure_ascii=False)

