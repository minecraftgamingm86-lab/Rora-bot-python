import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput


# ─────────────────────────────────────────
# EMBED BUILDER VIEW
# ─────────────────────────────────────────

class EmbedBuilder(View):
    def __init__(self, bot, embed: discord.Embed, author_id: int):
        super().__init__(timeout=600)
        self.bot = bot
        self.embed = embed
        self.author_id = author_id
        self.message = None

    async def interaction_check(self, interaction: discord.Interaction):

        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "❌ This embed builder isn't yours.",
                ephemeral=True
            )
            return False

        return True

    async def update_embed(self):

        if self.message:
            await self.message.edit(embed=self.embed, view=self)

    # ─────────────────────────────────────────
    # BUTTONS
    # ─────────────────────────────────────────

    @discord.ui.button(label="Title", style=discord.ButtonStyle.secondary)
    async def edit_title(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TitleModal(self))

    @discord.ui.button(label="Description", style=discord.ButtonStyle.secondary)
    async def edit_desc(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(DescriptionModal(self))

    @discord.ui.button(label="Footer", style=discord.ButtonStyle.secondary)
    async def edit_footer(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(FooterModal(self))

    @discord.ui.button(label="Author", style=discord.ButtonStyle.secondary)
    async def edit_author(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AuthorModal(self))

    @discord.ui.button(label="Color", style=discord.ButtonStyle.primary)
    async def edit_color(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ColorModal(self))

    @discord.ui.button(label="Image", style=discord.ButtonStyle.success)
    async def edit_image(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ImageModal(self))

    @discord.ui.button(label="Thumbnail", style=discord.ButtonStyle.success)
    async def edit_thumb(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(ThumbnailModal(self))

    @discord.ui.button(label="Send Embed 📤", style=discord.ButtonStyle.blurple)
    async def send_embed(self, interaction: discord.Interaction, button: Button):

        view = ChannelSelectView(self.embed, self.author_id, interaction.guild)

        await interaction.response.send_message(
            "Select channel to send embed:",
            view=view,
            ephemeral=True
        )


# ─────────────────────────────────────────
# CHANNEL SELECT
# ─────────────────────────────────────────

class ChannelSelectView(View):
    def __init__(self, embed, author_id, guild):

        super().__init__(timeout=180)
        self.add_item(ChannelSelect(embed, author_id, guild))


class ChannelSelect(Select):

    def __init__(self, embed, author_id, guild):

        options = [
            discord.SelectOption(label=ch.name, value=str(ch.id), emoji="📨")
            for ch in guild.text_channels
            if ch.permissions_for(guild.me).send_messages
        ][:25]

        super().__init__(
            placeholder="Choose channel...",
            min_values=1,
            max_values=1,
            options=options
        )

        self.embed = embed
        self.author_id = author_id

    async def callback(self, interaction: discord.Interaction):

        if interaction.user.id != self.author_id:
            return await interaction.response.send_message(
                "❌ This embed isn't yours.",
                ephemeral=True
            )

        channel_id = int(self.values[0])
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            return await interaction.response.send_message(
                "Channel not found.",
                ephemeral=True
            )

        await channel.send(embed=self.embed)

        await interaction.response.send_message(
            f"✅ Embed sent to {channel.mention}",
            ephemeral=True
        )


# ─────────────────────────────────────────
# MODALS
# ─────────────────────────────────────────

class TitleModal(Modal, title="Edit Title"):

    title_text = TextInput(label="Title", max_length=256)

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view
        self.title_text.default = view.embed.title

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.title = self.title_text.value
        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Title updated",
            ephemeral=True
        )


class DescriptionModal(Modal, title="Edit Description"):

    desc = TextInput(label="Description", style=discord.TextStyle.paragraph)

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view
        self.desc.default = view.embed.description

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.description = self.desc.value
        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Description updated",
            ephemeral=True
        )


class FooterModal(Modal, title="Edit Footer"):

    text = TextInput(label="Footer Text")
    icon = TextInput(label="Footer Icon URL", required=False)

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.set_footer(
            text=self.text.value,
            icon_url=self.icon.value if self.icon.value else None
        )

        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Footer updated",
            ephemeral=True
        )


class AuthorModal(Modal, title="Edit Author"):

    name = TextInput(label="Author Name")
    icon = TextInput(label="Author Icon URL", required=False)
    url = TextInput(label="Author URL", required=False)

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.set_author(
            name=self.name.value,
            icon_url=self.icon.value if self.icon.value else None,
            url=self.url.value if self.url.value else None
        )

        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Author updated",
            ephemeral=True
        )


class ColorModal(Modal, title="Set Color"):

    color = TextInput(label="Color HEX (#5865F2)")

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        value = self.color.value.replace("#", "")

        try:
            color = int(value, 16)
            self.view.embed.color = discord.Color(color)
        except:
            pass

        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Color updated",
            ephemeral=True
        )


class ImageModal(Modal, title="Set Image"):

    url = TextInput(label="Image URL")

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.set_image(url=self.url.value)

        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Image updated",
            ephemeral=True
        )


class ThumbnailModal(Modal, title="Set Thumbnail"):

    url = TextInput(label="Thumbnail URL")

    def __init__(self, view: EmbedBuilder):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):

        self.view.embed.set_thumbnail(url=self.url.value)

        await self.view.update_embed()

        await interaction.response.send_message(
            "✅ Thumbnail updated",
            ephemeral=True
        )


# ─────────────────────────────────────────
# COG
# ─────────────────────────────────────────

class EmbedBuilderCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="embed")
    @commands.has_permissions(manage_messages=True)

    async def embed(self, ctx):

        embed = discord.Embed(
            title="Example Title",
            description="Use the buttons to customize this embed.",
            color=discord.Color.blurple()
        )

        embed.set_footer(text="Created with +embed")

        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )

        view = EmbedBuilder(self.bot, embed, ctx.author.id)

        message = await ctx.send(embed=embed, view=view)

        view.message = message


async def setup(bot):

    await bot.add_cog(EmbedBuilderCog(bot))