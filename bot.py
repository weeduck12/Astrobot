import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv
import time

#charger le token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#intents 
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
#Création du bot 
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"astrobot awakened")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if "quoi" in message.content.lower():
        await message.channel.send("feur")

        await bot.process_commands(message)

bot.run(TOKEN)

