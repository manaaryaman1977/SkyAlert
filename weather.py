"""
Weather engine — uses Open-Meteo (free, no API key needed).
Fetches live conditions for every city and returns the best match.
"""

import httpx
import random
from typing import Optional

# WMO Weather Interpretation Codes → our condition buckets
# https://open-meteo.com/en/docs#weathervariables
WMO_MAP = {
    # clear
    0:  "clear",
    1:  "clear",
    # partly cloudy
    2:  "partly_cloudy",
    # cloudy / overcast
    3:  "cloudy",
    # fog
    45: "fog",
    48: "fog",
    # drizzle / light rain
    51: "rain", 53: "rain", 55: "rain",
    56: "rain", 57: "rain",
    # rain
    61: "rain", 63: "rain", 65: "rain",
    66: "rain", 67: "rain",
    # snow → treat as cloudy for India context
    71: "cloudy", 73: "cloudy", 75: "cloudy", 77: "cloudy",
    # showers
    80: "rain", 81: "rain", 82: "rain",
    # thunderstorm
    95: "storm",
    96: "storm", 99: "storm",
}


async def fetch_conditions(cities: list[dict]) -> list[dict]:
    """
    Batch-fetch current weather for all cities using Open-Meteo.
    Returns list of dicts: {name, lat, lon, condition, wmo_code, temp_c}
    """
    # Build a single bulk request using Open-Meteo's multi-location support
    lats = ",".join(str(c["lat"]) for c in cities)
    lons = ",".join(str(c["lon"]) for c in cities)

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lats}&longitude={lons}"
        "&current=temperature_2m,weathercode"
        "&timezone=auto"
        "&forecast_days=1"
    )

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

    # Open-Meteo returns a list when multiple locations are requested
    if isinstance(data, dict):
        data = [data]

    results = []
    for city, info in zip(cities, data):
        code = info.get("current", {}).get("weathercode", 0)
        temp = info.get("current", {}).get("temperature_2m", None)
        results.append({
            "name":      city["name"],
            "lat":       city["lat"],
            "lon":       city["lon"],
            "wmo_code":  code,
            "condition": WMO_MAP.get(code, "clear"),
            "temp_c":    temp,
        })

    return results


async def find_city_for_condition(
    cities: list[dict],
    wanted: str,
) -> Optional[dict]:
    """
    Fetch live weather for all cities, then return a random one
    that matches `wanted` condition.  Falls back to any city if
    no exact match is found (keeps the bot always functional).
    """
    live = await fetch_conditions(cities)

    if wanted == "any":
        return random.choice(live)

    matches = [c for c in live if c["condition"] == wanted]
    if matches:
        return random.choice(matches)

    # Graceful fallback: pick any city and note the mismatch internally
    return random.choice(live)
