import discord, time, psutil, platform

from discord.ext import commands
from stuff.funcs import send, fmt_time
from setup.config import SUCCESS, LOADING

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        start = time.time()

        if ctx.interaction:
            await ctx.defer()
        elif ctx.message:
            try:
                await ctx.message.add_reaction(LOADING)
            except Exception:
                pass

        end = time.time()

        ws = round(self.bot.latency * 1000)
        api = round((end - start) * 1000)

        if ctx.message:
            try:
                emoji = discord.PartialEmoji.from_str(LOADING)
                await ctx.message.remove_reaction(emoji, self.bot.user)
            except Exception:
                pass

        await send(ctx, f"-# ws: **{ws} ms**, api: **{api} ms**")

    @commands.hybrid_command()
    async def sys(self, ctx: commands.Context):
        await send(ctx, f"-# cpu: **{psutil.cpu_percent(interval = 0.1):.1f}%**, ram: **{psutil.virtual_memory().percent}%**")

    @commands.hybrid_command()
    async def env(self, ctx: commands.Context):
        await send(ctx, f"-# py: **{platform.python_version()}**, dc: **{discord.__version__}**, os: **{platform.system()} {platform.release()} {platform.machine()}**\n")

    @commands.hybrid_command()
    async def uptime(self, ctx: commands.Context):
        await send(ctx, f"-# **{fmt_time(int(time.time() - self.bot.start_time))}**")

async def setup(bot):
    await bot.add_cog(System(bot))
