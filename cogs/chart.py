import matplotlib.pyplot as plt
import io
from discord import File

async def send_stock_chart(ctx, stock_name):
    # Load historical prices from your DB
    history = db.table("history").get(Query().stock == stock_name)
    if not history:
        return await ctx.send("No history found for this stock.")

    times = history["timestamps"]
    prices = history["prices"]

    plt.figure(figsize=(8,4))
    plt.plot(times, prices, marker='o', linestyle='-', color='green')
    plt.title(f"{stock_name} Price Chart 📈")
    plt.xlabel("Time")
    plt.ylabel("Price (💰)")
    plt.grid(True)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    file = File(fp=buffer, filename=f"{stock_name}_chart.png")
    await ctx.send(file=file)
