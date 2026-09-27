"""
Central configuration loader for Raja Chor Bot.

Reads environment variables from .env and exposes typed constants
that every module in the bot imports from here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


# ─────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Load .env from project root
load_dotenv(ENV_FILE)


# ─────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────
def _require(key: str) -> str:
    """Return env var or raise if missing."""
    value = os.getenv(key)
    if value is None or value.strip() == "":
        raise RuntimeError(f"Missing required environment variable: {key}")
    return value.strip()


def _get_str(key: str, default: str) -> str:
    value = os.getenv(key)
    return value.strip() if value and value.strip() else default


def _get_int(key: str, default: int) -> int:
    value = os.getenv(key)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        raise RuntimeError(f"Environment variable {key} must be an integer, got: {value!r}")


# ─────────────────────────────────────────────────────────
# Telegram credentials
# ─────────────────────────────────────────────────────────
API_ID: int = _get_int("API_ID", 0)
if API_ID == 0:
    raise RuntimeError("API_ID is required. Get it from https://my.telegram.org")

API_HASH: str = _require("API_HASH")
BOT_TOKEN: str = _require("BOT_TOKEN")
BOT_USERNAME: str = _require("BOT_USERNAME")   # without leading @


# ─────────────────────────────────────────────────────────
# Database
# ─────────────────────────────────────────────────────────
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH: str = _get_str("DB_PATH", "data/scores.db")
DB_URL: str = f"sqlite:///{BASE_DIR / DB_PATH}"


# ─────────────────────────────────────────────────────────
# Game constants
# ─────────────────────────────────────────────────────────
MAX_PLAYERS: int = _get_int("MAX_PLAYERS", 4)
JOIN_TIMEOUT_SECONDS: int = _get_int("JOIN_TIMEOUT_SECONDS", 60)
PARCHI_PER_PLAYER: int = _get_int("PARCHI_PER_PLAYER", 4)

# Points
POINTS_WIN: int = _get_int("POINTS_WIN", 100)
POINTS_WRONG_WINNER: int = _get_int("POINTS_WRONG_WINNER", -50)


# ─────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────
LOG_LEVEL: str = _get_str("LOG_LEVEL", "INFO")


# ─────────────────────────────────────────────────────────
# Sanity check (only when run directly)
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("─── Raja Chor Bot Config ───")
    print(f"BASE_DIR            : {BASE_DIR}")
    print(f"API_ID              : {API_ID}")
    print(f"API_HASH            : {'*' * len(API_HASH)}")
    print(f"BOT_TOKEN           : {'*' * len(BOT_TOKEN)}")
    print(f"BOT_USERNAME        : {BOT_USERNAME}")
    print(f"DB_URL              : {DB_URL}")
    print(f"MAX_PLAYERS         : {MAX_PLAYERS}")
    print(f"JOIN_TIMEOUT_SECONDS: {JOIN_TIMEOUT_SECONDS}")
    print(f"PARCHI_PER_PLAYER   : {PARCHI_PER_PLAYER}")
    print(f"POINTS_WIN          : {POINTS_WIN}")
    print(f"POINTS_WRONG_WINNER : {POINTS_WRONG_WINNER}")
    print(f"LOG_LEVEL           : {LOG_LEVEL}")
