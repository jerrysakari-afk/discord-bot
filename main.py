@bot.event
async def on_message(message):
    # Älä reagoi botin omiin viesteihin
    if message.author.bot:
        return

    match = url_pattern.search(message.content)
    if match:
        url = match.group(1)

        # Tarkistetaan, ettei botti ole jo käsitellyt tätä viestiä
        if not url.startswith("steam://joinlobby/"):
            return

        encoded = urllib.parse.quote(url, safe="")
        redirect_url = f"{REDIRECT_BASE_URL}{encoded}"

        view = discord.ui.View()
        button = discord.ui.Button(
            label="Join Game 🎮",
            url=redirect_url,
            style=discord.ButtonStyle.link
        )
        view.add_item(button)

        # Lähetä vain kerran, älä poista alkuperäistä viestiä
        await message.channel.send(
            f"🎮 {message.author.mention} shared a Steam lobby:",
            view=view
        )

        return  # Estetään ylimääräinen event-triggeri

    await bot.process_commands(message)

