# SkyAlert Bot — Setup Guide

Everything you need to get the bot running in about 15 minutes.

---

## What you'll need

- A computer or a cheap VPS (even a free Oracle Cloud instance works)
- Python 3.10 or newer
- A Telegram account (both of you already have one)

---

## Step 1 — Create the Telegram bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Give it a name — something believable like `SkyAlert` or `India Weather Updates`
4. Give it a username — like `skyalert_in_bot`
5. BotFather replies with a **token** that looks like `7123456789:AAFxxx...`
6. Copy that token — you'll need it in Step 3

---

## Step 2 — Find your Telegram user IDs

Both of you need to do this once.

1. Open Telegram, search for **@userinfobot**
2. Send it any message
3. It replies with your numeric user ID — looks like `123456789`
4. Both of you send your IDs to each other so you can fill in the config

---

## Step 3 — Edit config.py

Open `config.py` and fill in:

```python
BOT_TOKEN    = "7123456789:AAFxxx..."   # from BotFather
YOUR_ID      = 123456789                 # your user ID
HER_ID       = 987654321                 # her user ID
YOUR_NAME    = "Your name"
HER_NAME     = "Her name"
```

Everything else (cities, messages, templates) can stay as-is or be customised however you like.

---

## Step 4 — Install and run

### On a computer (Mac / Linux)

```bash
# Clone or copy the weatherbot folder, then:
cd weatherbot

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

### On Windows

```bat
cd weatherbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

You should see:
```
INFO | Bot commands registered.
INFO | SkyAlert Bot is running…
```

---

## Step 5 — Both of you start the bot

1. Search for your bot's username on Telegram (e.g. `@skyalert_in_bot`)
2. Both of you send `/start`
3. The bot replies with a welcome message

Now either of you can type a command and the other person receives the bulletin.

---

## Step 6 — Keep it running 24/7 (optional but recommended)

If you run it on a VPS or your home computer, use `systemd` or `screen` to keep it alive.

### Simple way (screen):
```bash
screen -S skyalert
python bot.py
# Press Ctrl+A then D to detach
# Bot keeps running in background
```

### Proper way (systemd on Linux VPS):

Create `/etc/systemd/system/skyalert.service`:
```ini
[Unit]
Description=SkyAlert Telegram Bot
After=network.target

[Service]
User=YOUR_LINUX_USERNAME
WorkingDirectory=/path/to/weatherbot
ExecStart=/path/to/weatherbot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable skyalert
sudo systemctl start skyalert
sudo systemctl status skyalert   # should say "active (running)"
```

---

## Command reference

| Command     | Meaning (private) |
|-------------|-------------------|
| `/clear`    | I'm happy |
| `/clouds`   | I'm thinking about you |
| `/overcast` | I want to talk |
| `/rain`     | I miss you |
| `/storm`    | I really miss you |
| `/rainbow`  | You made my day |
| `/night`    | Good night |
| `/fog`      | I'm lost without you |
| `/status`   | See live weather for all cities (only you two see this) |
| `/help`     | Show the command list with meanings |

---

## How it works

1. You type `/rain`
2. Bot fetches live weather from Open-Meteo (free, no API key) for all 20 cities
3. It finds cities where it's actually raining right now
4. Picks one randomly
5. Generates a realistic bulletin:
   ```
   🌧  RAIN ADVISORY
   ────────────────────────────────
   Light rainfall has begun over Kochi.
   Roads may become slippery during evening hours.
   Current temperature: 27.3°C

   Issued: 18:45 IST, 14 Jul 2025
   Source: SkyAlert Meteorological Service
   ```
6. Sends it to the other person
7. Confirms to you which city was picked

If no city has matching weather (rare), it picks any city and still generates a natural-looking bulletin.

---

## Customising the secret language

Edit the `MESSAGES` dict in `config.py`. You can add new commands, change meanings, change anything:

```python
"snow": {
    "emoji":     "❄️",
    "label":     "Cold Wave Advisory",
    "condition": "cloudy",       # snow is rare in India so map to cloudy
    "meaning":   "I'm feeling cold without you.",
},
```

Then add the handler in `bot.py`:
```python
async def cmd_snow(u, c): await send_alert(u, c, "snow")
# and in main():
app.add_handler(CommandHandler("snow", cmd_snow))
```

---

## Free hosting options

If you don't want to leave your computer on:

- **Oracle Cloud Free Tier** — free VPS forever, enough for this bot
- **Railway.app** — free tier works for low-traffic bots
- **Fly.io** — free tier, easy to deploy
- **Render.com** — free background workers

All of these can run a Python process 24/7 for free.

---

## Troubleshooting

**Bot doesn't respond:**
- Make sure you both sent `/start` to the bot first
- Check that `YOUR_ID` and `HER_ID` are correct integers (no quotes)
- Confirm the bot token is correct

**Weather fetch fails:**
- Open-Meteo is free and needs no key — if it fails, it's a temporary outage
- Bot will show "temporarily unavailable" and you can try again

**Bot stops when you close the terminal:**
- Use `screen` or set up `systemd` as described above
