import discord
from discord.ext import commands
import time

from helpers.funcs import send, fmt_time, online, is_staff, ts
from setup.config import EMBED_COLOR, LOADING, SUCCESS

def register_commands(bot):
    @bot.command()
    async def crash(ctx):
        1/0

    @bot.command()
    async def ping(ctx):
        start = time.perf_counter()
        msg = await ctx.send("Pinging...")
        end = time.perf_counter()

        latency = round((end - start) * 1000)

        gateway = round(bot.latency * 1000)

        await msg.edit(
            content=f"Pong!\nLatency: `{latency}ms`\nAPI heartbeat: `{gateway}ms`"
        )

# yes its incomplete, what did you expect from the first version LMAOOO
