import discord
from discord.ext import commands
import aiosqlite
import database

class World(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="enter world")
    async def enter_world(self, ctx, world_name: str):
        active_pass = await database.get_active_passes(ctx.author.id)

        if active_pass is None:
            await ctx.send("You don't have any active passes. Please purchase a pass to enter the world.")
            return
        
        zone = await database.get_random_zone(active_pass['world_id'])
        character = await database.get_random_character(zone['id'])
        
        embed = discord.Embed(
            title=f"entered {world_name}!",
            description=f" {character['name']} is near..."
        )
        embed.set_image(url=zone['url'])
        embed.set_thumbnail(url=character['url'])

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")
        await msg.add_reaction("💥")

        if active_pass['expires_at'] is None:
            await database.activate_pass(ctx.author.id, active_pass['id'], 1)

def setup(bot): 
    bot.add_cog(World(bot))


