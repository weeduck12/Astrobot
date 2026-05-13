import discord
from discord.ext import commands
import aiosqlite
import random
import database

class Inventory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="inventory", description="Check your inventory")
    async def inventory(self, ctx):
        items = await database.get_user_items(ctx.author.id)
        if not items:
            await ctx.send("Your inventory is empty.")
            return
        
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Inventory", color=discord.Color.green())
        for item in items:
            embed.add_field(name=item['name'], value=f"Type: {item['type']}\nQuantity: {item['quantity']}", inline=False)
        
        await ctx.send(embed=embed)

def setup(bot): 
    bot.add_cog(Inventory(bot))