import discord 
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
load_dotenv()
import database
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())



@bot.event
async def on_ready():
    print(f'{bot.user} is booting up...')
    await database.init_db()

async def load_extensions():
    await bot.load_extension("cogs.greetings")
    await bot.load_extension("cogs.admin")
    await bot.load_extension("cogs.summon")
    await bot.load_extension("cogs.world")
    await bot.load_extension("cogs.inventory")

async def main():
    await load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())
