from discord.ext.commands.converter import UserConverter
from discord.ext.commands import ConversionError
from discord.ext import commands
from discord import Forbidden, HTTPException
import discord

from repositories.client_repo import ClientRepo
from repositories.karma_repo import KarmaRepo
from repositories.guild_repo import GuildRepo

from models.base_model import DB

from asyncio import sleep

from utils.constants import DEFAULT_AVAIABLE_KARMA, \
                            DEFAULT_AVAIABLE_KARMA_COOLDOWN, MAXIMUM_PAGE_SIZE, \
                            DEFAULT_PAGE_SIZE

class Karma(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.userConverter = UserConverter()
        self.clientRepo = ClientRepo()
        self.karmaRepo = KarmaRepo()
        self.guildRepo = GuildRepo()

    async def start_cooldown(self):
        while True:
            await sleep(DEFAULT_AVAIABLE_KARMA_COOLDOWN)
            self.karmaRepo.restart_avaiable_karma()

    async def behave(self, ctx):
        user = ctx.message.content[:-2:] # Remove the ++
        action = ctx.message.content[-2::] # Get the ++ or --

        try:
            user = await self.userConverter.convert(ctx, user)
        except ConversionError:
            await ctx.send("Wrong user given!")
            return
        
        giver_id = int(ctx.message.author.id)
        given_id = int(user.id)

        if giver_id == given_id:
            await ctx.send("Giving karma to yourself, what a faggot.")
            return

        guild = ctx.message.guild

        try:
            userObj = await guild.fetch_member(given_id)
        except (Forbidden, HTTPException):
            await ctx.send("Cannot fetch given user!")
            return
        
        if not userObj:
            await ctx.send("User is not in this server!")
            return

        giver_id = str(giver_id)
        given_id = str(given_id)
        guild_id = str(guild.id)


        with DB.transaction() as transaction:
            try:
                if not self.guildRepo.check_guild(guild_id):
                    self.guildRepo.insert_guild(guild_id, guild.name)

                if not self.clientRepo.check_user(giver_id):
                    self.clientRepo.insert_user(giver_id, ctx.message.author.name)

                if not self.clientRepo.check_user(given_id):
                    self.clientRepo.insert_user(given_id, user.name)

                if not self.karmaRepo.check_user_has_karma(giver_id, guild_id):
                    self.karmaRepo.create_karma(giver_id, guild_id)

                if not self.karmaRepo.check_user_has_karma(given_id, guild_id):
                    self.karmaRepo.create_karma(given_id, guild_id)
            except Exception as e:
                transaction.rollback()
                raise e

        if self.karmaRepo.get_user_avaiable_karma(giver_id, guild_id) <= 0:
            await ctx.send("You wasted your avaiable karma for this 24 hours.")
            return

        if action == "++":
            self.karmaRepo.give_karma(giver_id, given_id, guild_id)
            await ctx.send("Karma given!")
        elif action == "--":
            self.karmaRepo.take_karma(giver_id, given_id, guild_id)
            await ctx.send("Karma taken!")


    @commands.command(name="leaderboard", aliases=["topkarma", "topranking", "top"])
    async def topkarma(self, ctx, *args):
        pageSize = DEFAULT_PAGE_SIZE
        pageNum = 1 # First page default

        len_ = len(args)

        if len_ >= 1:
            isOK = True
            try:
                pageSize = int(args[0])
            except ValueError:
                await ctx.send("Wrong leaderboard size!")
                isOK = False

            if pageSize > MAXIMUM_PAGE_SIZE:
                await ctx.send(f"Too big leaderboard required, maximum is {MAXIMUM_PAGE_SIZE}")
                isOK = False

            if not isOK:
                return

            if len_ == 2:
                try:
                    pageNum = int(args[1])
                except ValueError:
                    await ctx.send("Wrong page chosen!")
                    isOK = False

                if not isOK:
                    return

        topKarma = self.karmaRepo.get_top_karma_server(ctx.message.guild.id, pageSize, pageNum)

        if not topKarma:
            await ctx.send("Your server has no karma records :(")
            return

        index = (pageNum * pageSize) - (pageSize - 1)
        result = discord.Embed(title=f"Top karma in {ctx.message.guild.name}", color=0x00ff24)
        result.set_thumbnail(url=ctx.message.guild.icon_url)
        for karma in topKarma:
            result.add_field(name=karma.client.current_name, value=str(index) + ". " + str(karma.karma), inline=False)
            index += 1

        await ctx.send(embed=result)
    
    @commands.command(name="karma", aliases=["mykarma", "mystats"])
    async def mykarma(self, ctx, *args):
        len_ = len(args)
        if len_ == 0:
            givenUser = ctx.message.author
            karma = self.karmaRepo.get_user_karma(str(ctx.message.guild.id), str(givenUser.id))
        elif len_ == 1:
            isOK = True

            try:
                givenUser = await self.userConverter.convert(ctx, args[0])
            except (HTTPException, Forbidden):
                await ctx.send("Cannot fetch member!")
                isOK = False

            if not isOK:
                return

            if not givenUser:
                await ctx.send("Invalid user!")
                return

            karma = self.karmaRepo.get_user_karma(str(ctx.message.guild.id), str(givenUser.id))
        else:
            return

        if karma is None:
            await ctx.send("I dont know you.")
            return

        result = discord.Embed(title=f"{ctx.message.guild.name} karma of {givenUser.name}", color=0x00ff24)
        result.set_thumbnail(url=givenUser.avatar_url)
        result.add_field(name="Karma", value=str(karma.karma))
        result.add_field(name="Giftable karma", value=str(karma.avaiable_karma))

        await ctx.send(embed=result)

    @commands.command(name="karmaworld", aliases=["karmaoverall", "karmaall", "karmaglobal"])
    async def karmaglobal(self, ctx, *args):
        karma = self.karmaRepo.get_user_karma_all(str(ctx.message.author.id))

        if not karma.karmaSum:
            await ctx.send("I dont have any karma records :(")
            return

        user = ctx.message.author

        result = discord.Embed(title=f"Global karma of {user.name}", color=0x00ff24)
        result.set_thumbnail(url=user.avatar_url)
        result.add_field(name="Karma", value=str(karma.karmaSum))
        await ctx.send(embed=result)
