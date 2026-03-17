import discord
from discord.ext import commands
from discord.ui import View, Modal, TextInput, Select
import json
import os

FILE = "events_data.json"


# ─────────────────────────────
# DATA
# ─────────────────────────────

def load_events():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)


def save_events(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ─────────────────────────────
# EMBED BUILDER
# ─────────────────────────────

def build_embed():

    events = load_events()

    embed = discord.Embed(
        title="BABYMONSTER Upcoming Events",
        color=discord.Color.pink()
    )

    if not events:
        embed.description = "No upcoming events."

    for i, e in enumerate(events, start=1):

        embed.add_field(
            name=f"{i}. {e['title']}",
            value=f"📅 {e['date']}\n⏰ {e['time']}",
            inline=False
        )

    return embed


# ─────────────────────────────
# EVENT EDITOR VIEW
# ─────────────────────────────

class EventEditor(View):

    def __init__(self, author_id):

        super().__init__(timeout=600)

        self.author_id = author_id
        self.title = "New Event"
        self.date = "Not set"
        self.time = "Not set"
        self.message = None


    async def interaction_check(self, interaction):

        if interaction.user.id != self.author_id:

            await interaction.response.send_message(
                "This editor isn't yours.",
                ephemeral=True
            )

            return False

        return True


    async def update(self):

        embed = discord.Embed(
            title="Event Editor",
            color=discord.Color.blurple()
        )

        embed.add_field(name="Title", value=self.title, inline=False)
        embed.add_field(name="Date", value=self.date, inline=True)
        embed.add_field(name="Time", value=self.time, inline=True)

        embed.set_footer(text="Edit event then press Save")

        await self.message.edit(embed=embed, view=self)


    # ─────────────────────────────
    # BUTTONS
    # ─────────────────────────────

    @discord.ui.button(label="Edit Title")

    async def title_btn(self, interaction, button):
        await interaction.response.send_modal(TitleModal(self))


    @discord.ui.button(label="Edit Date")

    async def date_btn(self, interaction, button):
        await interaction.response.send_modal(DateModal(self))


    @discord.ui.button(label="Edit Time")

    async def time_btn(self, interaction, button):
        await interaction.response.send_modal(TimeModal(self))


    @discord.ui.button(label="Save Event", style=discord.ButtonStyle.green)

    async def save_btn(self, interaction, button):

        events = load_events()

        events.append({
            "title": self.title,
            "date": self.date,
            "time": self.time
        })

        save_events(events)

        await interaction.response.send_message(
            "Event saved!",
            ephemeral=True
        )


    @discord.ui.button(label="Remove Event", style=discord.ButtonStyle.red)

    async def remove_btn(self, interaction, button):

        events = load_events()

        if not events:

            return await interaction.response.send_message(
                "No events to remove.",
                ephemeral=True
            )

        view = RemoveEventView(self.author_id)

        await interaction.response.send_message(
            "Select event to remove:",
            view=view,
            ephemeral=True
        )


# ─────────────────────────────
# REMOVE EVENT SELECT
# ─────────────────────────────

class RemoveEventView(View):

    def __init__(self, author_id):

        super().__init__(timeout=180)
        self.add_item(RemoveEventSelect(author_id))


class RemoveEventSelect(Select):

    def __init__(self, author_id):

        self.author_id = author_id

        events = load_events()

        options = []

        for i, e in enumerate(events):

            options.append(
                discord.SelectOption(
                    label=e["title"],
                    description=f"{e['date']} | {e['time']}",
                    value=str(i)
                )
            )

        super().__init__(
            placeholder="Choose event to remove",
            options=options
        )


    async def callback(self, interaction):

        if interaction.user.id != self.author_id:

            return await interaction.response.send_message(
                "Not your editor.",
                ephemeral=True
            )

        events = load_events()

        index = int(self.values[0])

        removed = events.pop(index)

        save_events(events)

        await interaction.response.send_message(
            f"Removed event: **{removed['title']}**",
            ephemeral=True
        )


# ─────────────────────────────
# MODALS
# ─────────────────────────────

class TitleModal(Modal, title="Event Title"):

    text = TextInput(label="Title")

    def __init__(self, editor):
        super().__init__()
        self.editor = editor

    async def on_submit(self, interaction):

        self.editor.title = self.text.value

        await self.editor.update()

        await interaction.response.send_message(
            "Title updated",
            ephemeral=True
        )


class DateModal(Modal, title="Event Date"):

    text = TextInput(label="Date")

    def __init__(self, editor):
        super().__init__()
        self.editor = editor

    async def on_submit(self, interaction):

        self.editor.date = self.text.value

        await self.editor.update()

        await interaction.response.send_message(
            "Date updated",
            ephemeral=True
        )


class TimeModal(Modal, title="Event Time"):

    text = TextInput(label="Time")

    def __init__(self, editor):
        super().__init__()
        self.editor = editor

    async def on_submit(self, interaction):

        self.editor.time = self.text.value

        await self.editor.update()

        await interaction.response.send_message(
            "Time updated",
            ephemeral=True
        )


# ─────────────────────────────
# COG
# ─────────────────────────────

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()

    async def addevents(self, ctx):

        editor = EventEditor(ctx.author.id)

        embed = discord.Embed(
            title="Event Editor",
            description="Create or remove events.",
            color=discord.Color.blurple()
        )

        msg = await ctx.send(embed=embed, view=editor)

        editor.message = msg


    @commands.command()

    async def events(self, ctx):

        embed = build_embed()

        await ctx.send(embed=embed)


async def setup(bot):

    await bot.add_cog(Events(bot))