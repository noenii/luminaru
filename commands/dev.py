import discord, time, asyncio, os, sys

from discord.ext import commands
from datetime import datetime, timedelta, timezone
from stuff.funcs import embed, send

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.is_owner()
    async def restart(self, ctx):
        await send(ctx, "restarting... gimme a sec")
        self.bot.dev_logger.info(f"Command: {ctx.command}, Requested by: {ctx.author}, Channel: {ctx.channel}")
        print("Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @commands.hybrid_command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await send(ctx, "ok bro")

        async def close():
            await asyncio.sleep(0)
            await self.bot.close()

        asyncio.create_task(close())

    '''
    unfinished
    @commands.command()
    async def reload()

    @commands.command()
    async def reloadall()

    @commands.command()
    async def load()

    @commands.command()
    async def unload()

    @commands.command()
    async def sync()

    @commands.command()
    async def extensions()

    @commands.command()
    async def logs()
    '''

async def setup(bot):
    await bot.add_cog(Dev(bot))
