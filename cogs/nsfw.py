import discord
from discord.ext import commands

from utils.pornhub_parser import PornhubParser


class Nsfw(commands.Cog):

    pornhubParser = None

    def __init__(self, bot):
        self.pornhubParser = PornhubParser()
        self.bot = bot

    @commands.command(name="nut")
    async def nut(self, ctx, *args):
        try:
            orientation = args[0]
        except IndexError:
            orientation = None

        link = await self.pornhubParser.get_pornhub_link(orientation)
        await ctx.send(link)
