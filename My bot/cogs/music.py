import discord
from discord.ext import commands
import yt_dlp
import asyncio

YDL_OPTIONS = {
    "format": "bestaudio/best",
    "quiet": True,
    "noplaylist": True
}

FFMPEG_OPTIONS = {
    "options": "-vn"
}


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    async def play_next(self, ctx):

        if ctx.guild.id not in self.queues:
            return

        if len(self.queues[ctx.guild.id]) == 0:
            return

        search = self.queues[ctx.guild.id].pop(0)

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{search}", download=False)["entries"][0]
            url = info["url"]
            title = info["title"]

        vc = ctx.voice_client

        source = await discord.FFmpegOpusAudio.from_probe(url)

        def after_playing(error):
            asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

        vc.play(source, after=after_playing)

        embed = discord.Embed(
            title="🎶 Now Playing",
            description=title,
            color=discord.Color.pink()
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def play(self, ctx, *, search: str):

        if ctx.author.voice is None:
            await ctx.send("❌ Join a voice channel first.")
            return

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            await voice_channel.connect()

        if ctx.guild.id not in self.queues:
            self.queues[ctx.guild.id] = []

        self.queues[ctx.guild.id].append(search)

        await ctx.send(f"📥 Added to queue: **{search}**")

        vc = ctx.voice_client

        if not vc.is_playing():
            await self.play_next(ctx)

    @commands.command()
    async def skip(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("⏭ Skipped the song.")

    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸ Music paused.")

    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶ Music resumed.")

    @commands.command()
    async def stop(self, ctx):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
            self.queues[ctx.guild.id] = []
            await ctx.send("⏹ Music stopped and queue cleared.")

    @commands.command()
    async def queue(self, ctx):

        if ctx.guild.id not in self.queues or len(self.queues[ctx.guild.id]) == 0:
            await ctx.send("📭 Queue is empty.")
            return

        msg = ""

        for i, song in enumerate(self.queues[ctx.guild.id]):
            msg += f"{i+1}. {song}\n"

        embed = discord.Embed(
            title="🎵 Music Queue",
            description=msg,
            color=discord.Color.purple()
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))