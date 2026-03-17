# cogs/moderation.py
import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class Moderation(commands.Cog):
    """Simple moderation commands with + prefix"""

    def __init__(self, bot):
        self.bot = bot

    async def can_act(self, target: discord.Member, actor: discord.Member) -> tuple[bool, str]:
        if target == self.bot.user:
            return False, "I can't moderate myself"
        if target == actor:
            return False, "You can't target yourself"
        if target.top_role >= actor.top_role and not actor.guild_permissions.administrator:
            return False, "Target has same or higher role than you"
        if target.top_role >= target.guild.me.top_role:
            return False, "My role is too low to moderate this user"
        return True, ""

    @commands.hybrid_command(name="kick", description="Kick a member")
    @app_commands.describe(member="User to kick", reason="Reason (optional)")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str] = None):
        allowed, msg = await self.can_act(member, ctx.author)
        if not allowed:
            return await ctx.send(msg, ephemeral=True)

        try:
            await member.kick(reason=reason or f"By {ctx.author}")
            await ctx.send(f"{member.mention} **kicked** successfully.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)

    @commands.hybrid_command(name="ban", description="Ban a member")
    @app_commands.describe(member="User to ban", reason="Reason (optional)", days="Delete messages 0-7 days old")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, reason: Optional[str] = None, days: int = 0):
        if days < 0 or days > 7:
            return await ctx.send("Days must be 0 to 7", ephemeral=True)

        allowed, msg = await self.can_act(member, ctx.author)
        if not allowed:
            return await ctx.send(msg, ephemeral=True)

        try:
            await ctx.guild.ban(member, reason=reason or f"By {ctx.author}", delete_message_days=days)
            await ctx.send(f"{member.mention} **banned** successfully.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)

    @commands.hybrid_command(name="mute", description="Mute / timeout a member")
    @app_commands.describe(member="User to mute", minutes="Time in minutes", reason="Reason (optional)")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, minutes: int, reason: Optional[str] = None):
        if minutes < 1:
            return await ctx.send("Minutes must be at least 1", ephemeral=True)

        allowed, msg = await self.can_act(member, ctx.author)
        if not allowed:
            return await ctx.send(msg, ephemeral=True)

        try:
            until = discord.utils.utcnow() + discord.utils.timedelta(minutes=minutes)
            await member.timeout(until, reason=reason or f"By {ctx.author}")
            await ctx.send(f"{member.mention} **muted** for {minutes} minutes.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)

    @commands.hybrid_command(name="unmute", description="Unmute a member")
    @app_commands.describe(member="User to unmute", reason="Reason (optional)")
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member, reason: Optional[str] = None):
        if member.timed_out_until is None:
            return await ctx.send(f"{member.mention} is not muted.")

        try:
            await member.timeout(None, reason=reason or f"By {ctx.author}")
            await ctx.send(f"{member.mention} **unmuted**.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)

    @commands.hybrid_command(name="purge", aliases=["clear"], description="Delete last N messages")
    @app_commands.describe(amount="Number of messages (max 100)")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx: commands.Context, amount: int):
        if amount < 1 or amount > 500:
            return await ctx.send("Amount must be between 1 and 500", ephemeral=True)

        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 = command message
            await ctx.send(f"Deleted **{len(deleted)-1}** messages.", delete_after=6)
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user_id: int, *, reason: Optional[str] = None):
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason or f"By {ctx.author}")
            await ctx.send(f"Unbanned **{user}** (ID: {user_id})")
        except discord.NotFound:
            await ctx.send("User not found in ban list.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Moderation(bot))