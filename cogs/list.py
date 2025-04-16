import discord
from discord.ext import commands
import json

# Load penguin facts from JSON file with proper encoding
with open('./data/penguinFacts.json', 'r', encoding='utf-8') as file:
    penguin_facts = json.load(file)

class ListPenguins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="list", description="Lists penguin species with filter options")
    async def list_penguins(self, interaction: discord.Interaction, filter: str):
        """
        Lists penguin species with filter options.
        :param interaction: The interaction object.
        :param filter: The filter option ('all' or 'endangered').
        """
        try:
            if filter == 'all':
                # Show all species
                title = 'List of All Penguin Species'
                filtered_penguins = '\n'.join(
                    f"{penguin['emoji']} {penguin['commonName']}" for penguin in penguin_facts.values()
                )
            elif filter == 'endangered':
                # Show only endangered species
                title = 'List of Endangered Penguin Species'
                filtered_penguins = '\n'.join(
                    f"{penguin['emoji']} {penguin['commonName']}" for penguin in penguin_facts.values()
                    if penguin['redListStatus'] == 'Endangered'
                )
            else:
                await interaction.response.send_message('Invalid filter option. Please choose "all" or "endangered".')
                return

            await interaction.response.send_message(f"**{title}** 🐧\n\n{filtered_penguins}")
        except Exception as error:
            print(error)
            await interaction.response.send_message('There was an error while executing this command!')

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(ListPenguins(bot))
