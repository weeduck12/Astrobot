import discord
from discord.ext import commands
import aiosqlite
import random
import database

class Summon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="summon")
    async def summon(self, ctx):
        async with aiosqlite.connect(database.DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT id FROM items WHERE type = 'pass'") as cursor:
                rows = await cursor.fetchall()
                
            if not rows:
                return await ctx.send("Database empty ! add some items first with *add_item")

            # On en choisit un au hasard
            random_id = random.choice(rows)['id']

            async with db.execute("SELECT * FROM items WHERE id = ?", (random_id,)) as cursor:
                item = await cursor.fetchone()

        embed = discord.Embed(
            title=f"🌀{item['name']}🌀", 
            description=item['description'], 
            color=discord.Color.blue()
        )
        embed.set_image(url=item['url']) # Image
        
        await ctx.send(content=f"**{ctx.author.display_name}** has opened a path...", embed=embed)

def setup(bot): 
    bot.add_cog(Summon(bot)) 