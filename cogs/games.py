# ───────────────────────── Casino UI ─────────────────────────

class CasinoView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=60)
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user.id == self.user_id

    @discord.ui.button(label="🎲 Dice", style=discord.ButtonStyle.primary)
    async def dice(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(self.user_id)
        roll = random.randint(1, 6)

        if roll >= 4:
            win = 50
            user["coins"] += win
            result = f"🎲 You rolled **{roll}** and won {win}💰!"
        else:
            lose = 30
            user["coins"] -= lose
            result = f"🎲 You rolled **{roll}** and lost {lose}💰!"

        update_user(self.user_id, {"coins": user["coins"]})
        await interaction.response.send_message(result, ephemeral=True)

    @discord.ui.button(label="🪙 Coin Flip", style=discord.ButtonStyle.success)
    async def coinflip(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(self.user_id)
        result = random.choice(["Heads", "Tails"])
        win = random.choice([True, False])

        if win:
            user["coins"] += 40
            msg = f"🪙 {result}! You won 40💰"
        else:
            user["coins"] -= 25
            msg = f"🪙 {result}! You lost 25💰"

        update_user(self.user_id, {"coins": user["coins"]})
        await interaction.response.send_message(msg, ephemeral=True)

    @discord.ui.button(label="🎰 Slots", style=discord.ButtonStyle.danger)
    async def slots(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(self.user_id)
        symbols = ["🍒", "🍋", "🍉", "⭐"]

        roll = [random.choice(symbols) for _ in range(3)]

        if roll[0] == roll[1] == roll[2]:
            win = 120
            user["coins"] += win
            result = f"{' | '.join(roll)}\n🎉 JACKPOT! +{win}💰"
        else:
            lose = 50
            user["coins"] -= lose
            result = f"{' | '.join(roll)}\n😢 You lost {lose}💰"

        update_user(self.user_id, {"coins": user["coins"]})
        await interaction.response.send_message(result, ephemeral=True)

    @discord.ui.button(label="🎡 Spin", style=discord.ButtonStyle.secondary)
    async def spin(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = get_user(self.user_id)

        outcomes = [100, 50, 20, -30, -50, 200]
        result = random.choice(outcomes)

        user["coins"] += result
        update_user(self.user_id, {"coins": user["coins"]})

        if result > 0:
            msg = f"🎡 You won {result}💰!"
        else:
            msg = f"🎡 You lost {abs(result)}💰!"

        await interaction.response.send_message(msg, ephemeral=True)

# ───────────────────────── Command ─────────────────────────

@commands.command(name="casino")
async def casino(self, ctx):
    embed = discord.Embed(
        title="🎰 Casino",
        description="Choose a game below:",
        color=0xe74c3c
    )

    embed.add_field(name="🎲 Dice", value="Roll dice to win coins", inline=False)
    embed.add_field(name="🪙 Coin Flip", value="Heads or tails luck", inline=False)
    embed.add_field(name="🎰 Slots", value="Match symbols to win big", inline=False)
    embed.add_field(name="🎡 Spin", value="Random rewards or loss", inline=False)

    view = CasinoView(ctx.author.id)
    await ctx.send(embed=embed, view=view)
