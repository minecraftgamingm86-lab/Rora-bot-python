import discord
from discord.ext import commands
from discord.ui import View, Button, Modal, TextInput
from tinydb import TinyDB, Query

db = TinyDB("mv.json")
mv_table = db.table("mvs")

# ────────────────────────────── UTIL ──────────────────────────────

def get_all_mvs():
    return mv_table.all()

# ────────────────────────────── ADD MODAL ──────────────────────────────

class AddMVModal(Modal, title="Add New MV"):
    title_input = TextInput(label="MV Title", placeholder="Ex: Batter Up")
    url_input = TextInput(label="YouTube URL", placeholder="https://youtube.com/...")

    async def on_submit(self, interaction: discord.Interaction):
        mv_table.insert({
            "title": self.title_input.value,
            "url": self.url_input.value
        })
        await interaction.response.send_message("✅ MV Added!", ephemeral=True)

# ────────────────────────────── DELETE VIEW ──────────────────────────────

class DeleteMVView(View):
    def __init__(self):
        super().__init__(timeout=60)
        self.refresh_buttons()

    def refresh_buttons(self):
        self.clear_items()
        mvs = get_all_mvs()

        if not mvs:
            self.add_item(Button(label="No MVs found", disabled=True))
            return

        for mv in mvs:
            btn = Button(label=f"❌ {mv['title']}", style=discord.ButtonStyle.danger)

            async def callback(interaction: discord.Interaction, mv=mv):
                mv_table.remove(Query().title == mv["title"])
                await interaction.response.send_message(f"🗑 Deleted {mv['title']}", ephemeral=True)

            btn.callback = callback
            self.add_item(btn)

# ────────────────────────────── EDIT VIEW ──────────────────────────────

class EditMVModal(Modal):
    def __init__(self, old_title):
        super().__init__(title=f"Edit {old_title}")
        self.old_title = old_title

        self.new_title = TextInput(label="New Title", default=old_title)
        self.new_url = TextInput(label="New URL")

        self.add_item(self.new_title)
        self.add_item(self.new_url)

    async def on_submit(self, interaction: discord.Interaction):
        mv_table.update({
            "title": self.new_title.value,
            "url": self.new_url.value
        }, Query().title == self.old_title)

        await interaction.response.send_message("✏️ MV Updated!", ephemeral=True)

class EditMVView(View):
    def __init__(self):
        super().__init__(timeout=60)
        self.refresh_buttons()

    def refresh_buttons(self):
        self.clear_items()
        mvs = get_all_mvs()

        if not mvs:
            self.add_item(Button(label="No MVs found", disabled=True))
            return

        for mv in mvs:
            btn = Button(label=f"✏️ {mv['title']}", style=discord.ButtonStyle.primary)

            async def callback(interaction: discord.Interaction, mv=mv):
                await interaction.response.send_modal(EditMVModal(mv["title"]))

            btn.callback = callback
            self.add_item(btn)

# ────────────────────────────── MAIN PANEL ──────────────────────────────

class MVPanel(View):
    def __init__(self):
        super().__init__(timeout=120)

    @discord.ui.button(label="➕ Add MV", style=discord.ButtonStyle.success)
    async def add_mv(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(AddMVModal())

    @discord.ui.button(label="✏️ Edit MV", style=discord.ButtonStyle.primary)
    async def edit_mv(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Select MV to edit:", view=EditMVView(), ephemeral=True)

    @discord.ui.button(label="🗑 Delete MV", style=discord.ButtonStyle.danger)
    async def delete_mv(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("Select MV to delete:", view=DeleteMVView(), ephemeral=True)

# ────────────────────────────── COG ──────────────────────────────

class MV(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ADMIN PANEL
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmv(self, ctx):
        embed = discord.Embed(
            title="🎬 MV Manager",
            description="Manage your Music Videos",
            color=0xff69b4
        )

        embed.add_field(name="➕ Add MV", value="Add new video", inline=False)
        embed.add_field(name="✏️ Edit MV", value="Modify existing MV", inline=False)
        embed.add_field(name="🗑 Delete MV", value="Remove MV", inline=False)

        await ctx.send(embed=embed, view=MVPanel())

    # PUBLIC COMMAND
    @commands.command()
    async def mv(self, ctx):
        mvs = get_all_mvs()

        if not mvs:
            return await ctx.send("❌ No MVs added yet.")

        embed = discord.Embed(
            title="🎥 BABYMONSTER MVs",
            color=0xff1493
        )

        for mv in mvs:
            embed.add_field(
                name=mv["title"],
                value=mv["url"],
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MV(bot))
