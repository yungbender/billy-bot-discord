import time
import datetime
import psutil
import subprocess
import discord

from discord.ext import commands
from utils.constants import CURRENT_VERSION

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.start_timestamp = time.time()
        self.up_since = datetime.date.fromtimestamp(self.start_timestamp).strftime("%A, %B %d, %Y %I:%M:%S")

    @commands.command(name="ping", aliases=["stats", "status", "state"])
    async def fetch_stats(self, ctx):
        current_time = time.time()
        uptime = datetime.timedelta(seconds=(current_time - self.start_timestamp))
        memory = psutil.virtual_memory()
 
        result = discord.Embed(title="Billy status", color=0x0)
        result.add_field(name="Ping", value=("%.2f" % self.bot.latency + "s"))
        result.add_field(name="Uptime", value=uptime)
        result.add_field(name="Memory usage", value=f"{round(memory.used / 1000000000, 2)} GB / {round(memory.total / 1000000000, 2)} GB")
        result.add_field(name="Up since", value=self.up_since)
        result.add_field(name="Version", value=CURRENT_VERSION)

        await ctx.send(embed=result)
