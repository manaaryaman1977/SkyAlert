# ============================================================
#  SkyAlert Bot — Configuration
#  Edit this file to personalise everything.
# ============================================================

import os
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

# --- Telegram credentials ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
YOUR_ID_RAW = os.environ.get("YOUR_ID")
HER_ID_RAW = os.environ.get("HER_ID")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set")
if not YOUR_ID_RAW:
    raise ValueError("YOUR_ID environment variable is not set")
if not HER_ID_RAW:
    raise ValueError("HER_ID environment variable is not set")

YOUR_ID = int(YOUR_ID_RAW)
HER_ID = int(HER_ID_RAW)

# YOUR_NAME / HER_NAME are used only in the /help text visible to each of you
YOUR_NAME    = "User"
HER_NAME     = "User"

# --- Timezone for bulletin timestamps ---
TIMEZONE     = "Asia/Kolkata"

# ============================================================
#  City pool — bot picks a real city matching live weather
# ============================================================
CITIES = [
    {"name": "Shimla",      "lat": 31.1048, "lon": 77.1734},
    {"name": "Darjeeling",  "lat": 27.0360, "lon": 88.2627},
    {"name": "Munnar",      "lat":  9.5916, "lon": 77.0596},
    {"name": "Coorg",       "lat": 12.3375, "lon": 75.8069},
    {"name": "Manali",      "lat": 32.2396, "lon": 77.1887},
    {"name": "Ooty",        "lat": 11.4102, "lon": 76.6950},
    {"name": "Kochi",       "lat":  9.9312, "lon": 76.2673},
    {"name": "Goa",         "lat": 15.2993, "lon": 74.1240},
    {"name": "Jaipur",      "lat": 26.9124, "lon": 75.7873},
    {"name": "Pune",        "lat": 18.5204, "lon": 73.8567},
    {"name": "Chennai",     "lat": 13.0827, "lon": 80.2707},
    {"name": "Hyderabad",   "lat": 17.3850, "lon": 78.4867},
    {"name": "Bengaluru",   "lat": 12.9716, "lon": 77.5946},
    {"name": "Mumbai",      "lat": 19.0760, "lon": 72.8777},
    {"name": "Delhi",       "lat": 28.6139, "lon": 77.2090},
    {"name": "Kolkata",     "lat": 22.5726, "lon": 88.3639},
    {"name": "Rishikesh",   "lat": 30.0869, "lon": 78.2676},
    {"name": "Varanasi",    "lat": 25.3176, "lon": 82.9739},
    {"name": "Agra",        "lat": 27.1767, "lon": 78.0081},
    {"name": "Ahmedabad",   "lat": 23.0225, "lon": 72.5714},
    # Expanded Cities (10 more cities to make 30)
    {"name": "Srinagar",    "lat": 34.0837, "lon": 74.7973},
    {"name": "Gulmarg",     "lat": 34.0489, "lon": 74.3804},
    {"name": "Leh",         "lat": 34.1526, "lon": 77.5771},
    {"name": "Cherrapunji", "lat": 25.2702, "lon": 91.7325},
    {"name": "Shillong",    "lat": 25.5788, "lon": 91.8833},
    {"name": "Pondicherry", "lat": 11.9416, "lon": 79.8083},
    {"name": "Kodaikanal",  "lat": 10.2381, "lon": 77.4892},
    {"name": "Jaisalmer",   "lat": 26.9157, "lon": 70.9083},
    {"name": "Udaipur",     "lat": 24.5854, "lon": 73.7125},
    {"name": "Bhopal",      "lat": 23.2599, "lon": 77.4126},
]

# ============================================================
#  Hidden message mapping
#  command   → the /command both of you type
#  emoji     → shown in bulletin header
#  condition → weather to look for (clear/partly_cloudy/cloudy/rain/storm/fog/any)
#  meaning   → your private meaning (stored here only, never transmitted)
# ============================================================
MESSAGES = {
    "clear": {
        "emoji":     "☀️",
        "label":     "Clear Sky Advisory",
        "condition": "clear",
        "meaning":   "Kya kar rahe jaanu😘",
    },
    "clouds": {
        "emoji":     "🌤",
        "label":     "Partly Cloudy Update",
        "condition": "partly_cloudy",
        "meaning":   "Aapki yaad aarahi jaan🥺",
    },
    "overcast": {
        "emoji":     "☁️",
        "label":     "Cloud Cover Alert",
        "condition": "cloudy",
        "meaning":   "I miss you jaanu🥲",
    },
    "rain": {
        "emoji":     "🌧",
        "label":     "Rain Advisory",
        "condition": "rain",
        "meaning":   "Aapke bina ro rahe, jaldi reply😭",
    },
    "storm": {
        "emoji":     "⛈",
        "label":     "Thunderstorm Warning",
        "condition": "storm",
        "meaning":   "Mera dil ro raha hai jaan❤️🩹",
    },
    "rainbow": {
        "emoji":     "🌈",
        "label":     "Post-Rain Visibility Report",
        "condition": "any",
        "meaning":   "Love you jaan💖",
    },
    "snow": {
        "emoji":     "❄️",
        "label":     "Cold Wave Advisory",
        "condition": "cloudy",
        "meaning":   "hamko cuddle karna hai baby🔥",
    },
    "heatwave": {
        "emoji":     "🥵",
        "label":     "Thermal Advisory",
        "condition": "clear",
        "meaning":   "Jaan ham uttejit ho rahe hai😈",
    },
}

# ============================================================
#  Bulletin templates — {city} is substituted at runtime
#  Add more variants for variety; one is chosen randomly.
# ============================================================
TEMPLATES = {
    "clear": [
        "Clear skies are persisting over {city}.\nExcellent visibility is expected through the day.",
        "Sunny conditions continue across {city}.\nNo precipitation anticipated in the near term.",
        "Bright and clear weather dominates {city} today.\nAtmospheric pressure remains stable.",
        "High-pressure systems have settled over {city}.\nPleasant, sunny conditions expected.",
    ],
    "partly_cloudy": [
        "Partial cloud cover has developed over {city}.\nMixed conditions expected through the afternoon.",
        "Scattered clouds are moving across {city}.\nBrief sunny intervals likely between cloud bands.",
        "Variable cloud cover reported over {city}.\nTemperatures remain seasonal.",
        "Cloud development is patchy across {city}.\nNo significant weather impact anticipated.",
    ],
    "cloudy": [
        "Heavy cloud cover is developing over {city}.\nOvercast conditions expected through late evening.",
        "Cloud formation has intensified across {city}.\nResidents should expect limited sunshine today.",
        "An overcast sky has settled over {city}.\nCloud ceiling is low; visibility may reduce slightly.",
        "Thick cloud bands are moving over {city}.\nDull, overcast conditions forecast for the region.",
    ],
    "rain": [
        "Light rainfall has begun over {city}.\nRoads may become slippery during evening hours.",
        "Moderate rainfall is being reported around {city}.\nResidents are advised to carry rain gear.",
        "Rainfall activity has picked up over {city}.\nVisibility may reduce temporarily in heavy spells.",
        "Rain has commenced across parts of {city}.\nOutdoor activities should be planned accordingly.",
        "Intermittent showers are occurring over {city}.\nDrainage systems are operating normally.",
    ],
    "storm": [
        "Thunderstorm activity has been detected over {city}.\nResidents are advised to remain indoors.",
        "Severe weather alert issued for {city}.\nLightning strikes reported in the vicinity.",
        "A thunderstorm system is intensifying over {city}.\nStrong winds and heavy rain are anticipated.",
        "Active thunderstorm cells have formed near {city}.\nAvoid open areas and elevated terrain.",
    ],
    "rainbow": [
        "Post-rainfall conditions over {city} are producing excellent visibility.\nClear spells expected as the system moves east.",
        "Improving conditions reported across {city} following earlier showers.\nResidual cloud clearing gradually.",
        "Weather has improved significantly over {city}.\nSkies are brightening after the morning rain.",
    ],
    "snow": [
        "Cold wind currents sweep through {city}.\nResidents are advised to dress warmly and stay indoors.",
        "A significant drop in temperature is reported over {city}.\nFrosty conditions are expected during overnight hours.",
        "Sub-zero temperatures developing in high-altitude zones of {city}.\nWinter advisory remains in effect.",
    ],
    "heatwave": [
        "High temperature warning issued for {city}.\nAvoid prolonged outdoor exposure during afternoon peak hours.",
        "Hot dry winds continue to dominate {city}.\nStay hydrated and remain indoors where possible.",
        "Above-average seasonal temperatures recorded in {city}.\nHeat index remains elevated.",
    ],
}
