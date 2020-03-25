import discord
import secrets
from bs4 import BeautifulSoup
import requests_async as requests
from asyncio import sleep

from discord.ext import commands
from utils.common import get_git_hash

from utils.constants import CURRENT_VERSION
from repositories.prefix_repo import PrefixRepo

CORONA_REFRESH_SECONDS = 60
CORONA_CHANNELS = [682718612179386388, 573634340525703168]

class Interaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixRepo = PrefixRepo()

    async def start_corona_cooldown(self):
        embedCz = discord.Embed()
        embedSk = discord.Embed()

        channels = []
        for channelId in CORONA_CHANNELS:
            channels.append(self.bot.get_channel(channelId))

        while True:
            eCz = await self._parse_czechia()

            if eCz.to_dict() != embedCz.to_dict():
                embedCz = eCz
                for channel in channels:
                    await channel.send(embed=embedCz)

            eSk = await self._parse_slovakia()

            if eSk.to_dict() != embedSk.to_dict():
                embedSk = eSk
                for channel in channels:
                    await channel.send(embed=embedSk)

            await sleep(CORONA_REFRESH_SECONDS)

    @commands.command(name="echo")
    async def echo(self, ctx, *args):
        await ctx.message.delete()
        message = " ".join(args)
        await ctx.send(message)

    @commands.command(name="helpme", aliases=["help", "introduce", "whoareyou"])
    async def send_help(self, ctx):
        prefix = self.bot._get_prefix(None, ctx.message)

        embed = discord.Embed(title="Introduction", description="My name is Billy, aniki. ", color=0xd300f7)
        embed.set_author(name="Developed by yungbender")
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/unanything/images/e/e1/Billy.jpg")
        embed.add_field(name=f"{prefix}ask <question>", value="I will answer your question ;).", inline=True)
        embed.add_field(name=f"{prefix}pick <choice1> <choice2> ... <choicen>", value="Picks a choice from given words.", inline=True)
        embed.add_field(name=f"{prefix}roll <max> / <min> <max>", value="Rolls a value from 0 to value or from max to min.", inline=True)
        embed.add_field(name=f"{prefix}echo <message>", value="Sends a given message.", inline=True)
        embed.add_field(name=f"{prefix}helpme / introduce / whoareyou", value="Sends this embed.", inline=True)
        embed.add_field(name=f"{prefix}dick", value="Let's see :GachiGASM:", inline=True)
        embed.add_field(name=f"{prefix}h", value="H", inline=True)
        embed.add_field(name=f"{prefix}obunga", value=";)", inline=True)
        embed.add_field(name=f"{prefix}nut", value="Sends you sexy video.", inline=True)
        embed.add_field(name=f"{prefix}status", value="Show hosting status.", inline=True)
        embed.add_field(name="Karma", value="Karma is given with tag of the user and \"++\" or \"--\".")
        embed.add_field(name=f"{prefix}leaderboard", value="Show top karma on this server.", inline=True)
        embed.add_field(name=f"{prefix}karma", value="Show you karma on this server.", inline=True)
        embed.add_field(name=f"{prefix}karmaworld", value="Show your overall karma what Billy thinks about you.", inline=True)
        embed.add_field(name=f"{prefix}pasta <name>", value="Show copypasta by given name.", inline=True)
        embed.add_field(name=f"{prefix}pastaadd <name> <pasta>", value="Add copypasta with given name.", inline=True)
        embed.add_field(name=f"{prefix}pastas", value="Show pastas avaiable.", inline=True)
        embed.add_field(name=f"{prefix}setprefix", value="Change prefix of commands.", inline=True)
        embed.add_field(name="Version", value=CURRENT_VERSION, inline=True)
        embed.add_field(name="Github", value=GIT)
        embed.set_footer(text="And many many more features that you just need to discover. Karma is restarted every 12 hours.")
        await ctx.send(embed=embed)

    @commands.command(name="billyprefix", aliases=["setprefix"])
    async def change_prefix(self, ctx, prefix: str):
        if len(prefix) > 64:
            await ctx.send("Prefix is too long!")
            return

        self.prefixRepo.insert_prefix(prefix, str(ctx.message.guild.id))
        await ctx.send("Prefix saved!")

    async def _parse_slovakia(self):
        resp = await requests.get("https://www.worldometers.info/coronavirus/")

        if resp.status_code >= 400:
            return None

        html = BeautifulSoup(resp.content, "html.parser")

        embed = discord.Embed(title="Slovakia")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/682718612179386388/692009072316121108/3x.png")

        sk_column = html.find("td", text="Slovakia").parent
        sk_column = sk_column.find_all("td")

        infected = sk_column[1].text if sk_column[1].text != "" else "0"
        newCases = sk_column[2].text if sk_column[2].text != "" else "0"
        recovered = sk_column[5].text if sk_column[5].test != "" else "0"

        embed.add_field(name="Infected", value=infected)
        embed.add_field(name="New cases", value=newCases)
        embed.add_field(name="Recovered", value=recovered)

        return embed

    async def _parse_czechia(self):
        resp = await requests.get("https://onemocneni-aktualne.mzcr.cz/covid-19")

        if resp.status_code >= 400:
        	return None

        html = BeautifulSoup(resp.content, "html.parser")

        embed = discord.Embed(title="Czechia")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/682718612179386388/692009221234884638/3x.png")

        tested = int(((html.find(id="count-test")).text).replace(" ", ""))
        infected = int(((html.find(id="count-sick")).text).replace(" ", ""))
        recovered = int(((html.find(id="count-recover")).text).replace(" ", ""))

        embed.add_field(name="Infected", value=str(infected))
        embed.add_field(name="Tested", value=str(tested))
        embed.add_field(name="Recovered", value=str(recovered))

        return embed

    @commands.command(name="corona", aliases=["coronachan"])
    async def corona_status(self, ctx):
        embed = await self._parse_slovakia()
        if embed:
            await ctx.send(embed=embed)

        embed = await self._parse_czechia()
        if embed:
            await ctx.send(embed=embed)
