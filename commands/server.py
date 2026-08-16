import discord

from discord.ext import commands
from stuff.funcs import send

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # needed: server, icon, banner, splash, emojis, stickers, sounds, channels, boosters,
    # features, owner, member count, invites, events, security, rules

    @commands.hybrid_command()
    async def server(self, ctx):
        await send(ctx, "yep")

async def setup(bot):
    await bot.add_cog(Server(bot))
