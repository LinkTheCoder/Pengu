import discord
from discord.ext import commands
import json
import unicodedata
import re

# Load penguin facts from the JSON file
with open('./data/penguinFacts.json', 'r', encoding='utf-8') as f:
    penguin_facts = json.load(f)

def normalize_string(s):
    # Normalize the string to remove accents and special characters
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8')
    # Replace spaces with hyphens and convert to lowercase
    s = s.replace(' ', '-').lower()
    return s

class Facts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='facts', description="Facts about selected penguin species")
    async def facts(self, interaction: discord.Interaction, *, species: str):
        user_input = species.lower()

        # Attempt to find an exact match
        matching_species = penguin_facts.get(user_input)

        # If no exact match is found, search for a match with "penguin" omitted
        if not matching_species:
            species_name = user_input.replace('penguin', '').strip()

            for key in penguin_facts:
                if species_name in normalize_string(key):
                    matching_species = penguin_facts[key]
                    break

        # Use a regular expression to match common name variations
        if not matching_species:
            for key in penguin_facts:
                normalized_key = normalize_string(key)
                regex = re.compile(rf"^{normalized_key.replace('penguin', '').strip()}\\b", re.IGNORECASE)
                if regex.search(normalize_string(user_input)):
                    matching_species = penguin_facts[key]
                    break

        if matching_species:
            emoji = matching_species.get('emoji', '')
            common_name = matching_species.get('commonName', 'Unknown')
            scientific_name = matching_species.get('scientificName', 'Unknown')
            fact = matching_species.get('fact', 'No fact available.')
            image_url = matching_species.get('imageURL', None)
            average_lifespan = matching_species.get('averageLifespan', 'Unknown')
            size = matching_species.get('size', 'Unknown')
            weight = matching_species.get('weight', 'Unknown')
            red_list_status = matching_species.get('redListStatus', 'Unknown')
            location = matching_species.get('location', 'Unknown')

            response = f"## {common_name} {emoji}\n"
            if image_url:
                file = discord.File(image_url, filename='image.png')
                response += f"{fact}\n\n"
                response += f"**Common Name:** {common_name}\n"
                response += f"**Scientific Name:** {scientific_name}\n"
                response += f"**Average Lifespan:** {average_lifespan}\n"
                response += f"**Size:** {size}\n"
                response += f"**Weight:** {weight}\n"
                response += f"**Location:** {location}\n"
                response += f"**Red List Status:** {red_list_status}\n"
                await interaction.response.send_message(response, file=file)
            else:
                response += f"{fact}\n\n"
                response += f"**Common Name:** {common_name}\n"
                response += f"**Scientific Name:** {scientific_name}\n"
                response += f"**Average Lifespan:** {average_lifespan}\n"
                response += f"**Size:** {size}\n"
                response += f"**Weight:** {weight}\n"
                response += f"**Location:** {location}\n"
                response += f"**Red List Status:** {red_list_status}\n"
                await interaction.response.send_message(response)
        else:
            await interaction.response.send_message("Sorry, I don't have information on that penguin species.")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(Facts(bot))