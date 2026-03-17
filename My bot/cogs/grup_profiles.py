import discord
from discord.ext import commands


class GroupProfile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def members(self, ctx):

        embed = discord.Embed(
            title="BABYMONSTER (베이비몬스터)",
            description=(
                "BABYMONSTER is a 7-member girl group under YG Entertainment.\n\n"
                "The group debuted on **April 1, 2024** with the mini album **BABYMONS7ER**.\n"
                "They were first introduced through the survival show **Last Evaluation**.\n\n"
                "The group consists of talented members from Korea, Japan and Thailand, "
                "known for strong vocals, rap and performance.\n\n"
                "**Fandom Name:** MONSTIEZ\n"
                "**Members:** Ruka, Pharita, Asa, Ahyeon, Rami, Rora, Chiquita"
            ),
            color=discord.Color.pink()
        )

        embed.add_field(
            name="Group Information",
            value=(
                "**Company:** YG Entertainment\n"
                "**Debut:** April 1, 2024\n"
                "**Members:** 7\n"
                "**Origin:** South Korea\n"
                "**Genres:** K-Pop, Hip Hop"
            ),
            inline=False
        )

        embed.add_field(
            name="Members",
            value="🦥 Ruka\n🦌 Pharita\n🐰 Asa\n🦋 Ahyeon\n🐬 Rami\n🐼 Rora\n🐈‍⬛ Chiquita",
            inline=False
        )

        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1058273361853169664/1475104969500790978/HBwqsa6aoAA-5H7.png?ex=69b89e4e&is=69b74cce&hm=070641dfe9bec56c1e677f3d6a5456403ea57bd7faffb87967849ef5d524d9e2&"
        )

        embed.set_footer(
            text="Use +member <name> to see individual member profiles"
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GroupProfile(bot))