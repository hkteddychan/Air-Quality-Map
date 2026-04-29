#!/usr/bin/env python3
"""Fetch Hong Kong Air Quality data from Open-Meteo."""
import urllib.request
import json
from datetime import datetime

OUTPUT_FILE = "air_quality.json"

def fetch_aq():
    """Fetch HK air quality from Open-Meteo (multiple locations)."""
    locations = [
        ("中環", 22.2808, 114.1588),
        ("觀塘", 22.3121, 114.2280),
        ("荃灣", 22.3707, 114.1113),
        ("元朗", 22.4469, 114.0323),
        ("東涌", 22.2890, 113.9428),
        ("將軍澳", 22.3158, 114.2647),
    ]
    
    results = []
    for name, lat, lon in locations:
        url = (f"https://air-quality-api.open-meteo.com/v1/air-quality"
               f"?latitude={lat}&longitude={lon}"
               f"&current=us_aqi,pm2_5,pm10,ozone"
               f"&hourly=us_aqi,pm2_5"
               f"&timezone=Asia/Hong_Kong&forecast_days=1")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode('utf-8'))
                current = data.get('current', {})
                results.append({
                    "location": name,
                    "lat": lat,
                    "lon": lon,
                    "us_aqi": current.get('us_aqi'),
                    "pm25": current.get('pm2_5'),
                    "pm10": current.get('pm10'),
                    "ozone": current.get('ozone'),
                })
        except Exception as e:
            print(f"Error fetching {name}: {e}")
    
    return results

def aqi_level(aqi):
    if aqi is None: return "未知"
    if aqi <= 50: return "良好"
    if aqi <= 100: return "中等"
    if aqi <= 150: return "敏感人士關注"
    if aqi <= 200: return "不健康"
    if aqi <= 300: return "非常不健康"
    return "危險"

def main():
    print(f"[{datetime.now().isoformat()}] Fetching HK air quality...")
    stations = fetch_aq()
    for s in stations:
        level = aqi_level(s['us_aqi'])
        print(f"  {s['location']}: AQI {s['us_aqi']} ({level}), PM2.5 {s['pm25']}")
    
    result = {
        "updated": datetime.utcnow().isoformat(),
        "source": "Open-Meteo (https://open-meteo.com/)",
        "stations": stations
    }
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"✅ Updated AQ data: {len(stations)} stations")

if __name__ == "__main__":
    main()
