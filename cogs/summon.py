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
            # On récupère tous les IDs des persos existants
            async with db.execute("SELECT id FROM characters") as cursor:
                rows = await cursor.fetchall()
                
            if not rows:
                return await ctx.send("La base de données est vide ! Utilise *add_char d'abord.")

            # On en choisit un au hasard
            random_id = random.choice(rows)[0]

            # On récupère les infos complètes de ce perso
            async with db.execute("SELECT * FROM characters WHERE id = ?", (random_id,)) as cursor:
                char = await cursor.fetchone()

        # Création d'un bel Embed (la carte du perso)
        embed = discord.Embed(
            title=f"✨ {char[1]}", # Nom
            description=f"Série : **{char[2]}**", # Série
            color=discord.Color.blue()
        )
        embed.set_image(url=char[3]) # Image
        
        # Affichage des statistiques
        stats = (
            f"❤️ HP: {char[4]} | 🛡️ DEF: {char[5]} | 🧪 RES: {char[7]}\n"
            f"⚔️ ATK: {char[8]} | ⚡ SPD: {char[12]}"
        )
        embed.add_field(name="Statistiques", value=stats, inline=False)
        
        await ctx.send(content=f"**{ctx.author.display_name}** has summoned...", embed=embed)

def setup(bot): # this is called by discord.py to setup the cog
    bot.add_cog(Summon(bot)) # add the cog to the bot