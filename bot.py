import discord 
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()
import database
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='*', intents=discord.Intents.all())



@bot.event
async def on_ready():
    print(f'{bot.user} is booting up...')
    await database.init_db()
bot.load_extension("cogs.greetings")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.summon")
bot.load_extension("cogs.world")
bot.run(TOKEN)
