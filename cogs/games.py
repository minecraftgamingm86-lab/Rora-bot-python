# cogs/economy.py
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput
from tinydb import TinyDB, Query
import random

db = TinyDB("economy.json")

# ────────────────────────────── User Registration ──────────────────────────────

def get_user(user_id):
    users = db.table("users")
    user = users.get(Query().id == user_id)
    if not user:
        users.insert({"id": user_id, "coins": 500, "cards": [], "level": 1, "xp": 0})
        user = users.get(Query().id == user_id)
    return user

def update_user(user_id, data):
    users = db.table("users")
    users.update(data, Query().id == user_id)

# ────────────────────────────── Shop System ──────────────────────────────

SHOP_ITEMS = [
    {"name": "Mystery Card", "price": 100},
    {"name": "Rare Card", "price": 500},
    {"name": "Legend Card", "price": 1200},
]

class ShopView(View):
    def __init__(self, user_id):
        super().__init__(timeout=300)
        self.user_id = user_id

    @discord.ui.button(label="Buy Item", style=discord.ButtonStyle.green)
    async def buy_item(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(BuyModal(self.user_id))

class BuyModal(Modal, title="Buy Item"):
    item_name = TextInput(label="Item Name", placeholder="Ex: Rare Card")
    quantity = TextInput(label="Quantity", placeholder="Ex: 2")

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        item = self.item_name.value.strip()
        qty = int(self.quantity.value.strip())
        user = get_user(self.user_id)
        matched = next((i for i in SHOP_ITEMS if i["name"].lower() == item.lower()), None)
        if not matched:
            return await interaction.response.send_message("Item not found in shop.", ephemeral=True)
        total_price = matched["price"] * qty
        if user["coins"] < total_price:
            return await interaction.response.send_message("Not enough coins.", ephemeral=True)
        # Deduct coins and add cards
        user["coins"] -= total_price
        user["cards"] += [matched["name"]] * qty
        update_user(self.user_id, {"coins": user["coins"], "cards": user["cards"]})
        await interaction.response.send_message(f"Bought {qty}x {item} for {total_price}💰", ephemeral=True)

# ────────────────────────────── Economy Cog ──────────────────────────────

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance")
    async def balance(self, ctx):
        user = get_user(ctx.author.id)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Wallet", color=0x1abc9c)
        embed.add_field(name="Coins", value=f"{user['coins']}💰")
        embed.add_field(name="Level", value=f"{user['level']}")
        embed.add_field(name="Cards Owned", value=f"{len(user['cards'])}")
        await ctx.send(embed=embed)

    @commands.command(name="daily")
    async def daily(self, ctx):
        from datetime import datetime, timedelta
        user = get_user(ctx.author.id)
        now = datetime.utcnow()
        last_claim = user.get("last_daily")
        if last_claim:
            last = datetime.fromisoformat(last_claim)
            if now - last < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last)
                return await ctx.send(f"⏳ Daily reward already claimed! Wait {remaining} hours.")
        # Give reward
        reward = random.randint(100, 500)
        user["coins"] += reward
        user["last_daily"] = now.isoformat()
        update_user(ctx.author.id, {"coins": user["coins"], "last_daily": user["last_daily"]})
        await ctx.send(f"🎉 You received {reward}💰 coins for your daily reward!")

    @commands.command(name="shop")
    async def shop(self, ctx):
        embed = discord.Embed(title="🛒 Shop", color=0xf1c40f)
        for item in SHOP_ITEMS:
            embed.add_field(name=item["name"], value=f"{item['price']}💰", inline=False)
        view = ShopView(ctx.author.id)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="cards")
    async def cards(self, ctx):
        user = get_user(ctx.author.id)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Cards", color=0x9b59b6)
        if user["cards"]:
            counts = {}
            for c in user["cards"]:
                counts[c] = counts.get(c, 0)+1
            for card, qty in counts.items():
                embed.add_field(name=card, value=f"{qty}x", inline=True)
        else:
            embed.description = "No cards owned yet!"
        await ctx.send(embed=embed)

    @commands.command(name="casino")
    async def casino(self, ctx):
        coins = get_user(ctx.author.id)["coins"]
        if coins < 10:
            return await ctx.send("You need at least 10💰 to play casino!")
        result = random.choice(["win", "lose"])
        bet = 50
        if result == "win":
            coins += bet
            update_user(ctx.author.id, {"coins": coins})
            await ctx.send(f"🎰 You won {bet}💰! You now have {coins}💰")
        else:
            coins -= bet
            update_user(ctx.author.id, {"coins": coins})
            await ctx.send(f"🎰 You lost {bet}💰! You now have {coins}💰")

async def setup(bot):
    await bot.add_cog(Economy(bot))
