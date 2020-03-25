import discord
import secrets
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="obunga")
    async def obunga(self, ctx):
        embed = discord.Embed()
        embed.set_image(url="https://i.imgur.com/R7hJie2.gif")
        await ctx.send(embed=embed)

    @commands.command(name="h")
    async def h(self, ctx):
        embed = discord.Embed()
        embed.set_image(url="https://i.imgur.com/0rqLzNY.jpg")
        await ctx.send(embed=embed)
