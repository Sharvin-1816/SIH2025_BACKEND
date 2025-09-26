import json

# Paths to individual JSON outputs
news_path = r"C:\SIH_BACKEND\External_data\scheme_news\news.json"
scheme_path = r"C:\SIH_BACKEND\External_data\scheme_news\schemes.json"
weather_path = r"C:\SIH_BACKEND\External_data\weather\weather.json"
log_path = r"C:\SIH_BACKEND\Log_data\metadata.json"   # assuming you save farm log result here

# Load JSON files
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

news_data = load_json(news_path)
scheme_data = load_json(scheme_path)
weather_data = load_json(weather_path)
log_data = load_json(log_path)

# Combine all into single JSON
final_data = {
    "news": news_data if news_data else [],
    "scheme": scheme_data if scheme_data else [],
    "weather": weather_data if weather_data else [],
    "log": log_data if log_data else {}
}

# Save combined JSON
output_path = r"C:\SIH_BACKEND\combined_data.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4, ensure_ascii=False)

print(f"✅ Combined JSON saved to {output_path}")
