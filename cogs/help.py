import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(
            title="BABYMONSTER Fan Bot Help",
            description="List of all available commands.",
            color=discord.Color.pink()
        )

        for cog_name, cog in self.bot.cogs.items():

            commands_list = []

            for command in cog.get_commands():

                if not command.hidden:
                    commands_list.append(f"`+{command.name}`")

            if commands_list:

                embed.add_field(
                    name=f"📂 {cog_name} Commands",
                    value=" • ".join(commands_list),
                    inline=False
                )

        embed.set_footer(text="Use +command for each feature")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))