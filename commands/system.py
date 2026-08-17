import discord, time, psutil, platform

from discord.ext import commands

from stuff.funcs import send, fmt_time

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
                await ctx.message.add_reaction("⭕")
            except Exception:
                pass

        end = time.time()

        ws = round(self.bot.latency * 1000)
        api = round((end - start) * 1000)

        if ctx.message:
            try:
                await ctx.message.remove_reaction("⭕", self.bot.user)
            except Exception:
                pass

        await send(ctx, f"-# WS: **{ws} ms**, API: **{api} ms**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def sys(self, ctx: commands.Context):
        await send(ctx, f"-# CPU: **{psutil.cpu_percent(interval = 0.1):.1f}%**, RAM: **{psutil.virtual_memory().percent}%**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def env(self, ctx: commands.Context):
        await send(ctx, f"-# Python: **{platform.python_version()}**, Discord.py: **{discord.__version__}**, OS: **{platform.system()} {platform.release()} {platform.machine()}**\n")

    @commands.hybrid_command()
    @commands.is_owner()
    async def uptime(self, ctx: commands.Context):
        await send(ctx, f"-# **{fmt_time(int(time.time() - self.bot.start_time))}**")

async def setup(bot):
    await bot.add_cog(System(bot))
