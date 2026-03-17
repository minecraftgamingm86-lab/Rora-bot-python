# cogs/market.py
import discord
from discord.ext import commands, tasks
from discord.ui import View, Button, Modal, TextInput, Select
from tinydb import TinyDB, Query
import random
from datetime import datetime, timedelta

db = TinyDB("market.json")

class InvestView(View):
    def __init__(self, user_id):
        super().__init__(timeout=600)
        self.user_id = user_id

    @discord.ui.button(label="Buy", style=discord.ButtonStyle.green)
    async def buy_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(BuyModal(self.user_id))

    @discord.ui.button(label="Sell", style=discord.ButtonStyle.red)
    async def sell_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(SellModal(self.user_id))

    @discord.ui.button(label="Stop-Loss", style=discord.ButtonStyle.secondary)
    async def stop_loss_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(StopLossModal(self.user_id))

class BuyModal(Modal, title="Buy Shares"):
    stock_name = TextInput(label="Stock Name", placeholder="Ex: Ruka")
    quantity = TextInput(label="Quantity", placeholder="Number of shares", style=discord.TextStyle.short)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        stock = self.stock_name.value.capitalize()
        qty = int(self.quantity.value)
        market_table = db.table("market")
        user_table = db.table("users")
        market = market_table.get(Query().id == 1)
        if not market or stock not in market:
            return await interaction.response.send_message("Invalid stock.", ephemeral=True)
        price = market[stock]*qty
        user = user_table.get(Query().id == self.user_id)
        if not user or user.get("coins",0)<price:
            return await interaction.response.send_message("Not enough coins.", ephemeral=True)
        # Deduct coins and add to portfolio
        portfolio = user.get("portfolio",{})
        portfolio[stock] = portfolio.get(stock,0)+qty
        user_table.update({"coins": user["coins"]-price,"portfolio":portfolio}, Query().id==self.user_id)
        await interaction.response.send_message(f"Bought {qty} shares of {stock} for {price}💰", ephemeral=True)

class SellModal(Modal, title="Sell Shares"):
    stock_name = TextInput(label="Stock Name", placeholder="Ex: Ruka")
    quantity = TextInput(label="Quantity", placeholder="Number of shares", style=discord.TextStyle.short)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        stock = self.stock_name.value.capitalize()
        qty = int(self.quantity.value)
        user_table = db.table("users")
        user = user_table.get(Query().id==self.user_id)
        portfolio = user.get("portfolio",{})
        if stock not in portfolio or portfolio[stock]<qty:
            return await interaction.response.send_message("You don't have that many shares.", ephemeral=True)
        # Sell
        market = db.table("market").get(Query().id==1)
        price = market[stock]*qty
        portfolio[stock]-=qty
        user_table.update({"coins": user["coins"]+price, "portfolio":portfolio}, Query().id==self.user_id)
        await interaction.response.send_message(f"Sold {qty} shares of {stock} for {price}💰", ephemeral=True)

class StopLossModal(Modal, title="Set Stop-Loss"):
    stock_name = TextInput(label="Stock Name", placeholder="Ex: Ruka")
    price_limit = TextInput(label="Sell if below this price", placeholder="Number", style=discord.TextStyle.short)

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def on_submit(self, interaction: discord.Interaction):
        stock = self.stock_name.value.capitalize()
        limit = int(self.price_limit.value)
        user_table = db.table("users")
        user = user_table.get(Query().id==self.user_id)
        stoploss = user.get("stoploss",{})
        stoploss[stock] = limit
        user_table.update({"stoploss": stoploss}, Query().id==self.user_id)
        await interaction.response.send_message(f"Stop-Loss set for {stock} at {limit}💰", ephemeral=True)

class Market(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.market_table = db.table("market")
        if not self.market_table.get(Query().id==1):
            # Initialize market prices
            self.market_table.insert({"id":1,"Ruka":100,"Asa":150,"Ahyeon":120,"Rami":80,"Rora":90,"Pharita":110,"Chiquita":70})
        self.fluctuate_prices.start()

    @tasks.loop(minutes=30)
    async def fluctuate_prices(self):
        market = self.market_table.get(Query().id==1)
        for k in market:
            if k=="id": continue
            change = random.randint(-10,15)
            market[k] = max(10,market[k]+change)
        self.market_table.update(market, Query().id==1)

    @commands.command(name="invest")
    async def invest(self, ctx):
        user_table = db.table("users")
        user = user_table.get(Query().id==ctx.author.id)
        if not user:
            user_table.insert({"id":ctx.author.id,"coins":500,"portfolio":{}, "stoploss":{}})
            user = user_table.get(Query().id==ctx.author.id)
        market = self.market_table.get(Query().id==1)
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Investment Panel", color=0x1abc9c)
        msg_text = "**Available Stocks:**\n"
        for stock, price in market.items():
            if stock=="id": continue
            qty = user.get("portfolio",{}).get(stock,0)
            msg_text += f"{stock}: {price}💰 | Owned: {qty}\n"
        embed.description = msg_text
        view = InvestView(ctx.author.id)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Market(bot))
