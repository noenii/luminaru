import discord

from discord.ext import commands
from stuff.funcs import send

class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # need channel info, perms, threads
    # slowmode and vc info as honorable mentions ig

    @commands.hybrid_command()
    async def channel(self, ctx):
        await send(ctx, "yep")

async def setup(bot):
    await bot.add_cog(Channel(bot))
