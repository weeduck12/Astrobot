import discord
from discord.ext import commands
import aiosqlite
import random
import database

class Summon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pending_claims = {}  # To track pending claims for items
    @commands.command(name="summon", description="Summon a random pass from the database")
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
        
        msg = await ctx.send(content=f"**{ctx.author.display_name}** has opened a path...", embed=embed)
        await msg.add_reaction("🌀") # Add a reaction to the message
        self.pending_claims[msg.id] = item['id'] # Store the item ID for this message

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
            if payload.user_id ==  self.bot.user.id:
                return
            if str(payload.emoji) == "🌀":
                item_id = self.pending_claims.get(payload.message_id)
                if item_id:
                    await database.add_pass_to_user(payload.user_id, item_id, 1)
                    channel = self.bot.get_channel(payload.channel_id)
                    await channel.send(f"<@{payload.user_id}> has claimed the pass!")

def setup(bot): 
    bot.add_cog(Summon(bot)) 