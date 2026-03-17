import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
import json
import os

WELCOME_FILE = "welcome_data.json"


def load_data():
    if not os.path.exists(WELCOME_FILE):
        return {}
    with open(WELCOME_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(WELCOME_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────
# SETUP VIEW
# ─────────────────────────────

class WelcomeBuilder(View):

    def __init__(self, bot, embed, author_id, guild_id):
        super().__init__(timeout=600)

        self.bot = bot
        self.embed = embed
        self.author_id = author_id
        self.guild_id = guild_id
        self.channel_id = None
        self.message = None

    async def interaction_check(self, interaction):

        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "This setup is not yours.",
                ephemeral=True
            )
            return False

        return True

    async def update(self):

        if self.message:
            await self.message.edit(embed=self.embed, view=self)

    # ─────────────────────────────
    # EDIT BUTTONS
    # ─────────────────────────────

    @discord.ui.button(label="Edit Title")
    async def title(self, interaction, button):
        await interaction.response.send_modal(TitleModal(self))

    @discord.ui.button(label="Edit Description")
    async def desc(self, interaction, button):
        await interaction.response.send_modal(DescModal(self))

    @discord.ui.button(label="Color")
    async def color(self, interaction, button):
        await interaction.response.send_modal(ColorModal(self))

    @discord.ui.button(label="Footer")
    async def footer(self, interaction, button):
        await interaction.response.send_modal(FooterModal(self))

    @discord.ui.button(label="Image")
    async def image(self, interaction, button):
        await interaction.response.send_modal(ImageModal(self))

    @discord.ui.button(label="Thumbnail")
    async def thumb(self, interaction, button):
        await interaction.response.send_modal(ThumbModal(self))

    # ─────────────────────────────
    # CHANNEL SELECT
    # ─────────────────────────────

    @discord.ui.button(label="Set Greet Channel", style=discord.ButtonStyle.green)

    async def set_channel(self, interaction, button):

        view = ChannelSelectView(self)
        await interaction.response.send_message(
            "Select the welcome channel:",
            view=view,
            ephemeral=True
        )

    # ─────────────────────────────
    # SAVE SYSTEM
    # ─────────────────────────────

    @discord.ui.button(label="Save Welcome", style=discord.ButtonStyle.blurple)

    async def save(self, interaction, button):

        if not self.channel_id:

            return await interaction.response.send_message(
                "Set a welcome channel first.",
                ephemeral=True
            )

        data = load_data()

        data[str(self.guild_id)] = {
            "channel": self.channel_id,
            "embed": self.embed.to_dict()
        }

        save_data(data)

        await interaction.response.send_message(
            "Welcome system saved!",
            ephemeral=True
        )


# ─────────────────────────────
# CHANNEL SELECT
# ─────────────────────────────

class ChannelSelectView(View):

    def __init__(self, builder):

        super().__init__(timeout=180)
        self.add_item(ChannelSelect(builder))


class ChannelSelect(Select):

    def __init__(self, builder):

        self.builder = builder
        guild = builder.bot.get_guild(builder.guild_id)

        options = [
            discord.SelectOption(label=c.name, value=str(c.id))
            for c in guild.text_channels
        ][:25]

        super().__init__(
            placeholder="Select welcome channel",
            options=options
        )

    async def callback(self, interaction):

        self.builder.channel_id = int(self.values[0])

        await interaction.response.send_message(
            f"Channel set!",
            ephemeral=True
        )


# ─────────────────────────────
# MODALS
# ─────────────────────────────

class TitleModal(Modal, title="Edit Title"):

    text = TextInput(label="Title")

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        self.builder.embed.title = self.text.value
        await self.builder.update()

        await interaction.response.send_message(
            "Title updated",
            ephemeral=True
        )


class DescModal(Modal, title="Edit Description"):

    text = TextInput(label="Description", style=discord.TextStyle.paragraph)

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        self.builder.embed.description = self.text.value
        await self.builder.update()

        await interaction.response.send_message(
            "Description updated",
            ephemeral=True
        )


class FooterModal(Modal, title="Footer"):

    text = TextInput(label="Footer")

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        self.builder.embed.set_footer(text=self.text.value)
        await self.builder.update()

        await interaction.response.send_message(
            "Footer updated",
            ephemeral=True
        )


class ColorModal(Modal, title="Color"):

    text = TextInput(label="Hex color (#5865F2)")

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        try:
            color = int(self.text.value.replace("#",""),16)
            self.builder.embed.color = discord.Color(color)
        except:
            pass

        await self.builder.update()

        await interaction.response.send_message(
            "Color updated",
            ephemeral=True
        )


class ImageModal(Modal, title="Image"):

    text = TextInput(label="Image URL")

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        self.builder.embed.set_image(url=self.text.value)

        await self.builder.update()

        await interaction.response.send_message(
            "Image updated",
            ephemeral=True
        )


class ThumbModal(Modal, title="Thumbnail"):

    text = TextInput(label="Thumbnail URL")

    def __init__(self, builder):
        super().__init__()
        self.builder = builder

    async def on_submit(self, interaction):

        self.builder.embed.set_thumbnail(url=self.text.value)

        await self.builder.update()

        await interaction.response.send_message(
            "Thumbnail updated",
            ephemeral=True
        )


# ─────────────────────────────
# COG
# ─────────────────────────────

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setupwelcome(self, ctx):

        embed = discord.Embed(
            title="Welcome System Setup",
            description="Edit the welcome message using buttons.\n\n"
                        "Variables:\n"
                        "`{user}` `{username}` `{server}` `{membercount}`",
            color=discord.Color.blurple()
        )

        builder = WelcomeBuilder(
            self.bot,
            embed,
            ctx.author.id,
            ctx.guild.id
        )

        msg = await ctx.send(embed=embed, view=builder)
        builder.message = msg


    @commands.Cog.listener()
    async def on_member_join(self, member):

        data = load_data()

        guild_data = data.get(str(member.guild.id))

        if not guild_data:
            return

        channel = member.guild.get_channel(guild_data["channel"])

        if not channel:
            return

        embed = discord.Embed.from_dict(guild_data["embed"])

        if embed.title:
            embed.title = embed.title.replace("{username}", member.name)

        if embed.description:
            embed.description = embed.description\
                .replace("{user}", member.mention)\
                .replace("{username}", member.name)\
                .replace("{server}", member.guild.name)\
                .replace("{membercount}", str(member.guild.member_count))

        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Welcome(bot))