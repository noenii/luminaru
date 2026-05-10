import discord
from discord.ext import commands

from helpers.funcs import send, fmt_time, online, is_staff, ts
from setup.config import EMBED_COLOR, LOADING, SUCCESS

def register_commands(bot):
    @bot.command()
    async def crash(ctx):
        1/0

    @bot.command()
    async def ping(ctx):
        print(round(bot.latency * 1000))

# yes its incomplete, what did you expect from the first version LMAOOO
