import discord
import secrets
from discord.ext import commands

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="flip")
    async def flip(self, ctx):
        result = secrets.choice([True, False])
        await ctx.send(result)

    @commands.command(name="question", aliases=["ask"])
    async def question(self, ctx):
        result = secrets.choice(["Yes, that is true.", "Bruh.", "Yes, sir.", "YEAH.", "No, that is false.", "Nah, dude.", "No, sir."])
        await ctx.send(result)

    @commands.command(name="pick")
    async def pick(self, ctx, *args):
        if len(args) < 2:
            await ctx.send("I need to pick from 2 or more arguments!")
            return
        choice = secrets.choice(args)
        await ctx.send(choice)

    @commands.command(name="roll")
    async def roll(self, ctx, *args):
        try:
            args = [int(arg) for arg in args]
        except ValueError:
            raise commands.BadArgument

        len_ = len(args)
        if len_ == 2:
            min_ = args[0]
            max_ = args[1]

            if max_ < min_:
                await ctx.send("BRUH!")
                return

            result = min_ + secrets.randbelow(max_ - min_)
        elif len_ == 1:
            result = secrets.randbelow(args[0])
        else:
            return

        await ctx.send(result)
    
    @commands.command(name="rng")
    async def rng(self, ctx):
        result = secrets.randbelow(32769)
        await ctx.send(result)
    
    @commands.command(name="dicksize", aliases=["dick"])
    async def dicksize(self, ctx):
        size = secrets.randbelow(41)

        if size < 12:
            result = "Your dick has " + str(size) + "cm " + "<:OMEGALUL:448640552083390465>"
        elif size >= 12 and size < 21:
            result = "Your dick has " + str(size) + "cm " + "<:gachiGASM:448641560213717033>"
        else:
            result = "Your dick has " + str(size) + "cm " + "<:monkaS:448641575006765057>"
        await ctx.send(result)
