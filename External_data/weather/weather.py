import requests
import json
from datetime import datetime

API_HOST = "open-weather13.p.rapidapi.com"
API_KEY = "2beace1d4fmshd652c14b0cb8972p12d5c2jsn171474c41d62"
districts = {
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Kollam": (8.8932, 76.6141),
    "Pathanamthitta": (9.2649, 76.7876),
    "Alappuzha": (9.4981, 76.3388),
    "Kottayam": (9.5916, 76.5223),
    "Idukki": (9.8436, 77.1471),
    "Ernakulam": (10.0356, 76.3675),
    "Thrissur": (10.5276, 76.2144),
    "Palakkad": (10.7867, 76.6548),
    "Malappuram": (11.0730, 76.0743),
    "Kozhikode": (11.2588, 75.7804),
    "Wayanad": (11.6850, 76.1319),
    "Kannur": (11.8745, 75.3704),
    "Kasaragod": (12.5000, 75.2000)
}

results = []

for district, (lat, lon) in districts.items():
    url = f"https://{API_HOST}/latlon"
    querystring = {
        "latitude": lat,
        "longitude": lon,
        "lang": "EN"
    }
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        results.append({
            "district": district,
            "error": f"Failed to fetch data ({response.status_code})"
        })
        continue

    data = response.json()
    if "weather" in data and len(data["weather"]) > 0:
        weather_info = data["weather"][0]
        main = weather_info.get("main", "")
        description = weather_info.get("description", "")
        temp = data.get("main", {}).get("temp")
        feels_like = data.get("main", {}).get("feels_like")
        humidity = data.get("main", {}).get("humidity")
        dt = datetime.fromtimestamp(data.get("dt", 0)).isoformat()
        temp_c = temp - 273.15 if temp is not None else None
        feels_like_c = feels_like - 273.15 if feels_like is not None else None
        results.append({
            "district": district,
            "time": dt,
            "temperature_c": round(temp_c, 2) if temp_c is not None else None,
            "feels_like_c": round(feels_like_c, 2) if feels_like_c is not None else None,
            "humidity": humidity,
            "weather": main,
            "description": description
        })
    else:
        results.append({
            "district": district,
            "error": "No weather data available"
        })

# Write results to a JSON file
output_file = r"C:\SIH_BACKEND\External_data\weather\weather.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

# Print confirmation
print(f"Weather data saved to {output_file}")
