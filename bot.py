import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an instance of Bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True  # Enable privileged intent
bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        await load_extensions()  # Await the coroutine to load extensions
        synced = await bot.tree.sync()  # Sync slash commands with Discord
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Fix token handling
token = os.getenv('DISCORD_BOT_TOKEN')
if not token:
    raise ValueError("No token found")

bot.run(token)
