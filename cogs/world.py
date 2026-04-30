import discord
from discord.ext import commands
import aiosqlite
import database

class World(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="enter_world")
    async def enter_world(self, ctx, world_name: str):
        pass

async def setup(bot): 
    bot.add_cog(World(bot)) 