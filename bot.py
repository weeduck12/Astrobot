import discord 
import os
from dotenv import load_dotenv
import random
load_dotenv()
from discord.ext import commands
import database

bot = commands.Bot(command_prefix='*')
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    await database.init_db()
    print(f'{bot.user} is booting up...')

    try:
        await bot.load_extension('cogs.summon')
        await bot.load_extension('cogs.admin')
        print("admin and  summon cogs loaded successfully.")
    except Exception as e:
        print(f"Error loading cogs: {e}")

bot.run(TOKEN)