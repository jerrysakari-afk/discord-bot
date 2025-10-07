import re
import urllib.parse
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

REDIRECT_BASE_URL = "https://OMA-NETLIFY-SIVU.netlify.app/?link="  # korvaa omallasi

url_pattern = re.compile(r"(steam://joinlobby/[^\s]+)")
processed = set()

@bot.event
async def on_ready():
    print(f"✅ Kirjauduttu sisään käyttäjänä: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.id in processed:
        return
    processed.add(message.id)

    matches = url_pattern.findall(message.content)
    if not matches:
        return

    for url in matches:
        encoded = urllib.parse.quote(url, safe="")
        redirect_url = f"{REDIRECT_BASE_URL}{encoded}"

        view = discord.ui.View()
        button = discord.ui.Button(
            label="Join Game 🎮",
            url=redirect_url,
            style=discord.ButtonStyle.link
        )
        view.add_item(button)

        await message.channel.send(
            f"🎮 {message.author.mention} shared a Steam lobby:",
            view=view
        )

TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ Virhe: TOKEN ei ole asetettu Renderissä!")
else:
    bot.run(TOKEN)

