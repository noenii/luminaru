import discord

from discord.ext import commands
from stuff.funcs import send

class empty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def donothing(self, ctx):
        await send(ctx, "yep")

async def setup(bot):
    await bot.add_cog(empty(bot))
