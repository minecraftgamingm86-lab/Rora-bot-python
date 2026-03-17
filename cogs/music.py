import discord
from discord.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------- JOIN --------
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
            await ctx.send("Joined voice channel ✅")
        else:
            await ctx.send("Join a voice channel first!")

    # -------- LEAVE --------
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left voice channel ❌")

    # -------- PLAY --------
    @commands.command()
    async def play(self, ctx, *, query):
        if not ctx.author.voice:
            return await ctx.send("Join a voice channel first!")

        channel = ctx.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()

        vc = ctx.voice_client

        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True
        }

        await ctx.send(f"Searching: {query} 🔍")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info['title']

        vc.stop()
        vc.play(discord.FFmpegPCMAudio(url))

        await ctx.send(f"Now playing: **{title}** 🎶")

    # -------- STOP --------
    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Stopped ⏹️")

    # -------- PAUSE --------
    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")

    # -------- RESUME --------
    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.resume()
            await ctx.send("Resumed ▶️")

# -------- SETUP --------
async def setup(bot):
    await bot.add_cog(Music(bot))
