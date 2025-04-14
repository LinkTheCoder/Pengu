import discord
from discord.ext import commands
import os
import requests

class GifCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="gif", description="Get a random penguin GIF!")
    async def gif(self, interaction: discord.Interaction):
        tenor_api_key = os.getenv('TENOR_API_KEY')
        if not tenor_api_key:
            await interaction.response.send_message("Tenor API key is missing!")
            return

        # Fetch a random penguin GIF from Tenor
        response = requests.get(
            f"https://tenor.googleapis.com/v2/search?q=penguin&key={tenor_api_key}&limit=1&random=true"
        )
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                gif_url = data["results"][0]["media_formats"]["gif"]["url"]
                await interaction.response.send_message(gif_url)
            else:
                await interaction.response.send_message("Couldn't find any penguin GIFs!")
        else:
            await interaction.response.send_message("Failed to fetch GIFs from Tenor!")

async def setup(bot):
    await bot.add_cog(GifCommand(bot))
