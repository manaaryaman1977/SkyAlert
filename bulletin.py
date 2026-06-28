"""
Bulletin generator — turns a city + condition into a realistic weather advisory.
"""

import random
import pytz
from datetime import datetime
from config import TIMEZONE, TEMPLATES, MESSAGES


def _now_str() -> str:
    tz  = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    return now.strftime("%H:%M IST, %d %b %Y")


def make_bulletin(command: str, city: dict) -> str:
    """
    Build a formatted weather bulletin string.

    command : key from MESSAGES (e.g. "rain")
    city    : dict with at least {"name": str, "temp_c": float|None}
    """
    msg_cfg   = MESSAGES[command]
    emoji     = msg_cfg["emoji"]
    label     = msg_cfg["label"]
    condition = msg_cfg["condition"]

    # Pick a random template for this command if it has custom templates, otherwise fall back to condition
    template_key = command if command in TEMPLATES else condition
    pool = TEMPLATES.get(template_key) or TEMPLATES.get("clear")
    body = random.choice(pool).format(city=city["name"])

    # Optional temperature line
    temp_line = ""
    if city.get("temp_c") is not None:
        temp_line = f"\nCurrent temperature: {city['temp_c']:.1f}°C"

    bulletin = (
        f"{emoji}  {label.upper()}\n"
        f"{'─' * 32}\n"
        f"{body}"
        f"{temp_line}\n\n"
        f"Issued: {_now_str()}\n"
        f"Source: SkyAlert Meteorological Service"
    )
    return bulletin
