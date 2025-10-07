import re
import urllib.parse
import discord
from discord.ext import commands
import os

# --- BOTIN ASETUKSET ---
intents = discord.Intents.default()
intents.message_content = True  # tarvitaan, jotta botti näkee viestien sisällön
bot = commands.Bot(command_prefix="!", intents=intents)

# --- MUUTA TÄMÄ OMAKSI NETLIFY-SIVUKSEKSI ---
REDIRECT_BASE_URL = "https://OMA-NETLIFY-SIVU.netlify.app/?link="

# Etsi steam:// linkit
url_pattern = re.compile(r'((?:https?|steam):\/\/[^\s]+)')

# --- BOTTI KÄYNNISTYY ---
@bot.event
async def on_ready():
    print(f"✅ Kirjauduttu sisään käyttäjänä: {bot.user}")

# --- KUUNTELEE VIESTEJÄ ---
@bot.event
async def on_message(message):
    # älä reagoi botin omiin viesteihin
    if message.author.bot:
        return

    match = url_pattern.search(message.content)
    if match:
        url = match.group(1)

        # käsittele vain oikeat steam://joinlobby linkit
        if not url.startswith("steam://joinlobby/"):
            return

        encoded = urllib.parse.quote(url, safe="")
        redirect_url = f"{REDIRECT_BASE_URL}{encoded}"

        # luodaan join-nappi
        view = discord.ui.View()
        button = discord.ui.Button(
            label="Join Game 🎮",
            url=redirect_url,
            style=discord.ButtonStyle.link
        )
        view.add_item(button)

        # lähetä vain yksi viesti
        await message.channel.send(
            f"🎮 {message.author.mention} shared a Steam lobby:",
            view=view
        )

        return

    # anna muiden komentojen toimia
    await bot.process_commands(message)


# --- KÄYNNISTYS ---
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ Virhe: TOKEN ei ole asetettu ympäristömuuttujaksi Renderissä!")
else:
    bot.run(TOKEN)

