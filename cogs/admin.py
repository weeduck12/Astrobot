import discord
from discord.ext import commands
import database

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_user_id = 1208156854350258258 # Ton ID

    @commands.command(name="add_char")
    async def add_char(self, ctx, name, series, url, hp:int, defense:int, sp_def:int, res:int, atk:int, atk_stam:int, sp_atk:int, sp_stam:int, speed:int):
        # Vérification si c'est bien toi
        if ctx.author.id != self.target_user_id:
            return await ctx.send("Tu n'as pas la permission !")

        try:
            await database.add_character(name, series, url, hp, defense, sp_def, res, atk, atk_stam, sp_atk, sp_stam, speed)
            await ctx.send(f"✅ **{name}** ({series}) a été ajouté à la base de données !")
        except Exception as e:
            await ctx.send(f"❌ Erreur lors de l'ajout : {e}")

def setup(bot): # this is called by discord.py to setup the cog
    bot.add_cog(Admin(bot)) # add the cog to the bot