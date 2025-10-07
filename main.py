import re
import urllib.parse
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

REDIRECT_BASE_URL = "https://tourmaline-lolly-4c1df2.netlify.app/?link="

url_pattern = re.compile(r'((?:https?|steam)://[^\s]+)')

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    match = url_pattern.search(message.content)
    if match:
        url = match.group(1)

        if url.startswith("steam://"):
            encoded = urllib.parse.quote(url, safe='')
            redirect_url = f"{REDIRECT_BASE_URL}{encoded}"

            view = discord.ui.View()
            button = discord.ui.Button(
                label="Join Game",
                url=redirect_url,
                style=discord.ButtonStyle.link
            )
            view.add_item(button)

            await message.channel.send(
                f"🎮 {message.author.mention} shared a Steam lobby:",
                view=view
            )
        else:
            view = discord.ui.View()
            button = discord.ui.Button(
                label="Join Game",
                url=url,
                style=discord.ButtonStyle.link
            )
            view.add_item(button)

            await message.channel.send(
                f"🔗 {message.author.mention} shared a game link:",
                view=view
            )

        await message.delete()

    await bot.process_commands(message)

bot.run(os.getenv("TOKEN"))
