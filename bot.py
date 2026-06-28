"""
SkyAlert Bot — main entry point.
Both users share the same command set; each message goes to the OTHER person.
"""

import logging
import asyncio
from telegram import Update, BotCommand
from telegram.ext import (
    Application, CommandHandler, ContextTypes, MessageHandler, filters
)
from telegram.constants import ParseMode

from config import BOT_TOKEN, YOUR_ID, HER_ID, YOUR_NAME, HER_NAME, CITIES, MESSAGES
from weather import find_city_for_condition
from bulletin import make_bulletin

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

ALLOWED = {YOUR_ID, HER_ID}

def other_person(sender_id: int) -> int:
    """Return the recipient ID given the sender."""
    return HER_ID if sender_id == YOUR_ID else YOUR_ID


def sender_name(sender_id: int) -> str:
    return YOUR_NAME if sender_id == YOUR_ID else HER_NAME


# ── Shared command handler ──────────────────────────────────────────────────

async def send_alert(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
    sender = update.effective_user.id

    if sender not in ALLOWED:
        return  # silently ignore strangers

    recipient_id = other_person(sender)
    cfg = MESSAGES[command]

    # Acknowledge to sender immediately
    await update.message.reply_text(
        f"📡 Fetching live weather data…\n"
        f"Locating a city with matching conditions."
    )

    try:
        city = await find_city_for_condition(CITIES, cfg["condition"])
        text = make_bulletin(command, city)

        # Send bulletin to the other person
        await context.bot.send_message(
            chat_id=recipient_id,
            text=text,
        )

        # Confirm to sender (privately — not visible to recipient)
        await update.message.reply_text(
            f"✅ Alert dispatched.\n"
            f"📍 City selected: {city['name']}"
        )
        log.info(
            "Alert '%s' sent from %s → %s (city: %s)",
            command, sender_name(sender), sender_name(recipient_id), city["name"]
        )

    except Exception as e:
        log.error("Failed to send alert: %s", e)
        await update.message.reply_text(
            "⚠️ Weather service temporarily unavailable. Please try again."
        )


# --- Commands are dynamically registered in main() from config.MESSAGES ---


# ── /start ──────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.id
    if sender not in ALLOWED:
        return

    name = sender_name(sender)
    await update.message.reply_text(
        f"🌤 SkyAlert Meteorological Service\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Welcome, {name}.\n\n"
        f"You are subscribed to live regional weather alerts.\n"
        f"Use /help to see available commands."
    )


# ── /help ───────────────────────────────────────────────────────────────────

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.id
    if sender not in ALLOWED:
        return

    lines = ["🌐 *SkyAlert — Command Reference*\n"]
    for key, cfg in MESSAGES.items():
        lines.append(f"{cfg['emoji']}  `/{key}` — {cfg['meaning']}")

    lines.append("\nEach command dispatches a live bulletin to the other subscriber.")
    await update.message.reply_text(
        "\n".join(lines), parse_mode=ParseMode.MARKDOWN
    )


# ── /status — shows live weather snapshot for all cities ───────────────────

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.id
    if sender not in ALLOWED:
        return

    await update.message.reply_text("🔄 Fetching live conditions for all cities…")

    from weather import fetch_conditions
    try:
        live = await fetch_conditions(CITIES)
        lines = ["📊 *Live Weather Snapshot*\n"]
        for c in live:
            cond = c["condition"].replace("_", " ").title()
            temp = f"{c['temp_c']:.0f}°C" if c["temp_c"] is not None else "—"
            lines.append(f"• {c['name']}: {cond}, {temp}")
        await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Could not fetch data: {e}")


# ── Ignore all non-command messages silently ────────────────────────────────

async def ignore_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # bot does not reply to plain text


# ── Setup & run ─────────────────────────────────────────────────────────────

async def post_init(application: Application):
    """Register bot commands so they appear in the Telegram menu."""
    commands = [BotCommand(key, cfg["meaning"]) for key, cfg in MESSAGES.items()]
    commands += [
        BotCommand("start",  "Start the bot"),
        BotCommand("help",   "Show command list"),
        BotCommand("status", "Live weather snapshot"),
    ]
    await application.bot.set_my_commands(commands)
    log.info("Bot commands registered.")


def main():
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Register standard command handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("status", cmd_status))

    # Dynamically register handlers for each weather command configured in config.py
    def make_handler(command_name: str):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await send_alert(update, context, command_name)
        return handler

    for cmd in MESSAGES.keys():
        app.add_handler(CommandHandler(cmd, make_handler(cmd)))

    # Silently ignore plain text
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ignore_text))

    log.info("SkyAlert Bot is running…")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
