# main.py
import asyncio
import discord
from discord.ext import commands
import logging
from pathlib import Path

# ─── Import config ────────────────────────────────────────────────
from config import Config

# ─── Logging setup ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s → %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("bot.main")

# ─── Intents ──────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members         = True
intents.voice_states    = True
intents.reactions       = True      # useful for future reaction roles / games

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=Config.PREFIX,
            intents=intents,
            help_command=None,              # we'll make custom help later
            owner_id=Config.OWNER_ID,
            case_insensitive=True,
            strip_after_prefix=True
        )
        self.config = Config

    async def setup_hook(self):
        # ─── Load all cogs ────────────────────────────────────────
        cog_folder = Path("cogs")
        if not cog_folder.exists():
            cog_folder.mkdir()

        for file in cog_folder.glob("*.py"):
            if file.name == "__init__.py":
                continue
            cog_name = f"cogs.{file.stem}"
            try:
                await self.load_extension(cog_name)
                logger.info(f"Loaded cog → {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load {cog_name} → {e}")

        # ─── Sync application commands (slash) ────────────────────
        try:
            if self.config.TEST_GUILD_ID:
                guild = discord.Object(id=self.config.TEST_GUILD_ID)
                self.tree.copy_global_to(guild=guild)
                await self.tree.sync(guild=guild)
                logger.info(f"Slash commands synced to test guild {self.config.TEST_GUILD_ID}")
            else:
                await self.tree.sync()
                logger.info("Global slash commands synced (may take up to 1 hour)")
        except Exception as e:
            logger.error(f"Slash sync failed → {e}")

    async def on_ready(self):
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"{self.command_prefix}help")
        await self.change_presence(activity=activity, status=discord.Status.online)

        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print(f"┃  Bot is online → {self.user.name}#{self.user.discriminator}  ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.MissingPermissions):
            return await ctx.send("You don't have permission to use this command.", delete_after=10)
        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send("I lack the required permissions.", delete_after=10)

        logger.error(f"Command error | {ctx.command} | {error}")
        if ctx.author.id == self.owner_id:
            await ctx.send(f"Error: ```{error}```", delete_after=20)


# ─── Start the bot ────────────────────────────────────────────────────
bot = MyBot()

async def main():
    async with bot:
        await bot.start(Config.TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")