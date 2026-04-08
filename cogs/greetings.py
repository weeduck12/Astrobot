import discord
from discord.ext import commands

class Greetings(commands.Cog): # create a class for our cog that inherits from commands.Cog
    # this class is used to create a cog, which is a module that can be added to the bot

    def __init__(self, bot): # this is a special method that is called when the cog is loaded
        self.bot = bot

    @commands.command() # creates a prefixed command
    async def hello(self, ctx): # all methods now must have both self and ctx parameters
        await ctx.send('Hello!')

    @commands.command()
    async def goodbye(self, ctx):
        await ctx.send('Goodbye!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.slash_command(name='ping', description='Check if the bot is alive')
    async def ping_slash(self, ctx):
        await ctx.respond('Pong! Slash command works!')

    @commands.command()
    async def greet(self, ctx, member: discord.Member):
        await ctx.send(f'{ctx.author.mention} says hello to {member.mention}!')

    
def setup(bot): # this is called by discord.py to setup the cog
    bot.add_cog(Greetings(bot)) # add the cog to the bot
