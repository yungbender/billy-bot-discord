import discord
from discord.ext import commands

from psycopg2 import IntegrityError

from repositories.pasta_repo import CopypastaRepo

class Copypasta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pastaRepo = CopypastaRepo()

    @commands.command(name="pasta")
    async def pasta(self, ctx, *, pastaName: str):
        pasta = self.pastaRepo.get_pasta_by_name(pastaName)

        if pasta:
            await ctx.send(pasta.content)
        else:
            await ctx.send("Pasta not found :(")

    @commands.command(name="pastaadd")
    async def pastaAdd(self, ctx, pastaName: str, *, pasta: str):
        try:
            self.pastaRepo.insert_pasta(pastaName, pasta)
            await ctx.send("Pasta added!")
        except IntegrityError:
            await ctx.send("Pasta with this name already exists!")

    @commands.command(name="pastas")
    async def pastas(self, ctx):
        pastas = self.pastaRepo.get_all_pastas()
        if pastas:
            embed = discord.Embed(title="Avaiable pastas")
            for pasta in pastas:
                embed.add_field(name=pasta.pasta_name, value=pasta.pasta_name, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("I have no pastas :(")

