import re
import urllib.parse
import discord
from discord.ext import commands
import os
import threading
from flask import Flask

# --- Keepalive-palvelin Renderin ilmaisversiota varten ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# --- Discord-botin asetukset ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Netlify redirect (vaihda oma osoite tähän) ---
REDIRECT_BASE_URL = "https://tourmaline-lolly-4c1df2.netlify.app/?link="

# Etsi vain Steam joinlobby -linkit
url_pattern = re.compile(r"(steam://joinlobby/[^\s]+)")
processed = set()

@bot.event
async def on_ready():
    print(f"✅ Kirjauduttu sisään käyttäjänä: {bot.user}")

@bot.event
async def on_message(message):
    print(f"💬 Viesti havaittu: {message.content}")

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

# --- Käynnistys ---
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ Virhe: TOKEN ei ole asetettu Renderissä!")
else:
    keep_alive()  # tämä pitää botin hengissä Renderissä
    bot.run(TOKEN)


