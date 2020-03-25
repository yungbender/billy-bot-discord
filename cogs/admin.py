import os
from discord.ext import commands

OWNER_ID = int(os.getenv("OWNER_ID", None))

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.disabledCogs = {}

    @commands.command(name="disable")
    async def disableCog(self, ctx, cogName: str):
        if await self.bot.is_owner(ctx.message.author):
            cog = self.bot.get_cog(cogName)
            self.bot.remove_cog(cogName)
            if not cog:
                await ctx.send("Cog does not exist.")
                return
            self.disabledCogs[cogName] = cog
            await ctx.send("Done, disabled.")

    @commands.command(name="enable")
    async def enableCog(self, ctx, cogName: str):
        if await self.bot.is_owner(ctx.message.author):
            cog = self.disabledCogs.get(cogName)
            if not cog:
                await ctx.send("Cog does not exist.")
                return
            self.bot.add_cog(cog)
            await ctx.send("Done, enabled.")

    @commands.command(name="karmacdrestart")
    async def restartCdKarma(self, ctx):
        if await self.bot.is_owner(ctx.message.author):
            karma = self.bot.get_cog("Karma")
            karma.karmaRepo.restart_avaiable_karma()
            await ctx.send("Avaiable karma restarted on request.")

    @commands.command(name="karmareset")
    async def restartKarmaServer(self, ctx):
        if await self.bot.is_owner(ctx.message.author):
            karma = self.bot.get_cog("Karma")
            karma.karmaRepo.reset_server_karma(str(ctx.message.guild.id))
            await ctx.send("Karma for everyone on this server restarted on request.")
