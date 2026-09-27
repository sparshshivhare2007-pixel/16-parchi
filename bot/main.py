"""
Entry point for the Raja Chor Bot.

Starts the Telethon client, initializes the database,
and registers all command/callback handlers.
"""

import logging

from telethon import TelegramClient

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    LOG_LEVEL,
)
from bot.db.session import init_db
from bot.handlers import register_all_handlers


# ─────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("raja-chor-bot")


# ─────────────────────────────────────────────────────────
# Client factory
# ─────────────────────────────────────────────────────────
def create_client() -> TelegramClient:
    """Create and return a Telethon client in bot mode."""
    client = TelegramClient(
        session="raja_chor_bot",
        api_id=API_ID,
        api_hash=API_HASH,
    )
    return client


# ─────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────
def main() -> None:
    log.info("Starting Raja Chor Bot...")

    # 1. Init database
    init_db()
    log.info("Database initialized.")

    # 2. Create client
    client = create_client()

    # 3. Register handlers
    register_all_handlers(client)
    log.info("All handlers registered.")

    # 4. Start bot
    client.start(bot_token=BOT_TOKEN)
    log.info("Bot is online. Press Ctrl+C to stop.")

    client.run_until_disconnected()


if __name__ == "__main__":
    main()
