import discord
from discord.ext import commands

members = {

"ruka": {
"stage_name": "Ruka (루카)",
"birth_name": "Kawai Ruka (河井瑠花)",
"position": "Main Dancer, Main Rapper",
"birthday": "March 20, 2002",
"zodiac": "Pisces",
"chinese_zodiac": "Horse",
"height": "N/A",
"weight": "N/A",
"blood": "O",
"mbti": "ISTJ & ISFP",
"nationality": "Japanese 🇯🇵",
"color": "Forest Green",
"emoji": "🦥",
"image": "https://cdn.discordapp.com/attachments/1065285482398888089/1453766901800108195/G9BXAe_a0AA4BvT.png?ex=69b8c62f&is=69b774af&hm=19f542bd1ee1768a4682dca9dea7c920dff680dac693b88cfddbbe3130048234&"
},

"pharita": {
"stage_name": "Pharita (파리타)",
"birth_name": "Pharita Chaikong (ภาริตา ไชยคง)",
"legal_name": "Pharita Boonpakdeethaveeyod (ภริตา บุญภักดีทวียศ)",
"position": "Vocalist",
"birthday": "August 26, 2005",
"zodiac": "Virgo",
"chinese_zodiac": "Rooster",
"height": "N/A",
"weight": "N/A",
"blood": "A",
"mbti": "INTP",
"nationality": "Thai 🇹🇭",
"color": "Red-Pink",
"emoji": "🦌",
"image": "https://cdn.discordapp.com/attachments/1070358631318569022/1456206701916196997/G9jyTtdasAA2Tq4.png?ex=69b914ac&is=69b7c32c&hm=6f167f484dac53e1a43dc354afebcb5f34c5c670eb59c348142f5b5d9ecce0d2&"
},

"asa": {
"stage_name": "Asa (아사)",
"birth_name": "Enami Asa (榎並杏紗)",
"korean_name": "Kim Asa (김아사)",
"position": "Main Rapper, Vocalist, Dancer",
"birthday": "April 17, 2006",
"zodiac": "Aries",
"chinese_zodiac": "Dog",
"height": "N/A",
"weight": "N/A",
"blood": "O",
"mbti": "ENFP (previously ENTP, INTP)",
"nationality": "Japanese 🇯🇵",
"color": "Verve Violet",
"emoji": "🐰",
"image": "https://cdn.discordapp.com/attachments/1065285507820572804/1453756157813461254/G9A747obkAADC9H.png?ex=69b8bc2d&is=69b76aad&hm=b303a40bf9f2fda0d24e0c82d61d2741347e8670b1f35f201bcfeed002104ef5&"
},

"ahyeon": {
"stage_name": "Ahyeon (아현)",
"birth_name": "Jung Ahyeon (정아현)",
"chinese_name": "Zhèng Yaxián (郑雅贤)",
"position": "Main Vocalist, Rapper, Dancer, Visual, Center",
"birthday": "April 11, 2007",
"zodiac": "Aries",
"chinese_zodiac": "Pig",
"height": "163 cm (5'4)",
"weight": "N/A",
"blood": "A",
"mbti": "ISTJ",
"nationality": "Korean 🇰🇷",
"color": "Bright Orange",
"emoji": "🦋",
"image": "https://cdn.discordapp.com/attachments/1064280545795780679/1454082489697177773/G9F6jLMbEAABsX4.png?ex=69b89a99&is=69b74919&hm=069fa3e1c2d0ff89b70565fc2fa70fb9bc08556a5f51e425cc565cdd5d2e841b&"
},

"rami": {
"stage_name": "Rami (라미)",
"birth_name": "Shin Haram (신하람)",
"position": "Main Vocalist",
"birthday": "October 17, 2007",
"zodiac": "Libra",
"chinese_zodiac": "Pig",
"height": "N/A",
"weight": "N/A",
"blood": "O",
"mbti": "INFJ",
"nationality": "Korean 🇰🇷",
"color": "Sky Blue",
"emoji": "🐬",
"image": "https://cdn.discordapp.com/attachments/1062797011478388777/1392593679151271966/GuwkInqWEAEum1x.jpg?ex=69b907ae&is=69b7b62e&hm=8bdba78f6e01e2fd8fc9f9cc6dbe25cc84fbf29f7ae992160fe39964a5bd9b26&"
},

"rora": {
"stage_name": "Rora (로라)",
"birth_name": "Lee Dain (이다인)",
"position": "Lead Vocalist, Visual",
"birthday": "August 14, 2008",
"zodiac": "Leo",
"chinese_zodiac": "Rat",
"height": "N/A",
"weight": "N/A",
"blood": "A",
"mbti": "INTP",
"nationality": "Korean 🇰🇷",
"color": "Lemon Yellow",
"emoji": "🐼",
"image": "https://cdn.discordapp.com/attachments/1065285495904555060/1454392999382618192/G9KWZcKagAAeV3I.png?ex=69b91308&is=69b7c188&hm=e6938f56bcb58346d1bf3fa055859e80e34247470720f436702d257c7e6cb537&"
},

"chiquita": {
"stage_name": "Chiquita (치키타)",
"birth_name": "Riracha Phondechaphiphat (ริราชา พรเดชาพิพัฒน์)",
"position": "Vocalist, Dancer, Rapper, Maknae",
"birthday": "February 17, 2009",
"zodiac": "Aquarius",
"chinese_zodiac": "Ox",
"height": "N/A",
"weight": "N/A",
"blood": "O",
"mbti": "ISTP",
"nationality": "Thai 🇹🇭",
"color": "Magenta-Pink",
"emoji": "🐈‍⬛",
"image": "https://cdn.discordapp.com/attachments/1066735332617375814/1453720785662509066/G9AtAhAb0AYJY-3.png?ex=69b89b3c&is=69b749bc&hm=fb7ed702472e66c3803a1f32ac8862e05189c6ef6fd8fb6d3049a24699753f97&"
}

}


class MemberProfiles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def member(self, ctx, name: str):

        name = name.lower()

        if name not in members:
            return await ctx.send("Member not found.")

        m = members[name]

        embed = discord.Embed(
            title=f"{m['stage_name']} Profile",
            color=discord.Color.pink()
        )

        embed.add_field(name="Birth Name", value=m["birth_name"], inline=False)

        if "legal_name" in m:
            embed.add_field(name="Legal Name", value=m["legal_name"], inline=False)

        if "korean_name" in m:
            embed.add_field(name="Korean Name", value=m["korean_name"], inline=False)

        if "chinese_name" in m:
            embed.add_field(name="Chinese Name", value=m["chinese_name"], inline=False)

        embed.add_field(name="Position", value=m["position"], inline=False)

        embed.add_field(name="Birthday", value=m["birthday"], inline=True)
        embed.add_field(name="Zodiac Sign", value=m["zodiac"], inline=True)
        embed.add_field(name="Chinese Zodiac", value=m["chinese_zodiac"], inline=True)

        embed.add_field(name="Height", value=m["height"], inline=True)
        embed.add_field(name="Weight", value=m["weight"], inline=True)
        embed.add_field(name="Blood Type", value=m["blood"], inline=True)

        embed.add_field(name="MBTI", value=m["mbti"], inline=True)
        embed.add_field(name="Nationality", value=m["nationality"], inline=True)

        embed.add_field(name="Representative Color", value=m["color"], inline=True)
        embed.add_field(name="Representative Emoji", value=m["emoji"], inline=True)

        embed.set_image(url=m["image"])

        embed.set_footer(text="BABYMONSTER Member Profile")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MemberProfiles(bot))