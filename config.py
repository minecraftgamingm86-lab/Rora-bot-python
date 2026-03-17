# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

class Config:
    # ─── Core bot settings ────────────────────────────────────────
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise ValueError("TOKEN not found in .env file")

    PREFIX = "+"
    OWNER_ID = int(os.getenv("OWNER_ID", "0")) or None

    # ─── Appearance / colors ──────────────────────────────────────
    EMBED_COLOR       = 0x5865F2   # blurple (discord-like)
    SUCCESS_COLOR     = 0x57F287
    ERROR_COLOR       = 0xED4245
    WARNING_COLOR     = 0xFEE75C

    # ─── Development & sync ───────────────────────────────────────
    TEST_GUILD_ID = None
    # TEST_GUILD_ID = 123456789012345678   # ← uncomment & change to your test server ID for fast slash sync

    # ─── Database (will be used later for levels, warns, economy, etc.) ───
    DB_PATH = "data/bot_data.db"

    # You can add more settings later (api keys, channels, etc.)