import discord, time, psutil, platform, asyncio, os, sys, colorama

from discord.ext import commands
from colorama import Fore, Style

from stuff.funcs import fmt_time
from setup.config import ROOT

colorama.init(autoreset = True)

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

        await ctx.send(f"-# WS: **{ws} ms**, API: **{api} ms**")

        if ctx.message:
            try:
                await ctx.message.remove_reaction("⭕", self.bot.user)
            except Exception:
                pass

    @commands.hybrid_command()
    @commands.is_owner()
    async def sys(self, ctx: commands.Context):
        await ctx.send(f"-# CPU: **{psutil.cpu_percent(interval = 0.1):.1f}%**, RAM: **{psutil.virtual_memory().percent}%**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def env(self, ctx: commands.Context):
        await ctx.send(f"-# Python: **{platform.python_version()}**, Discord.py: **{discord.__version__}**, OS: **{platform.system()} {platform.release()} {platform.machine()}**\n")

    @commands.hybrid_command()
    @commands.is_owner()
    async def uptime(self, ctx: commands.Context):
        await ctx.send(f"-# **{fmt_time(int(time.time() - self.bot.start_time))}**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("-# Shutting Down")
        print(Style.BRIGHT + Fore.MAGENTA + "[DEV] Bot Shutdown")

        async def close():
            await asyncio.sleep(0)
            await self.bot.close()

        asyncio.create_task(close())

    @commands.hybrid_command()
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("-# Restarting...")
        print(Style.BRIGHT + Fore.MAGENTA + "[DEV] Bot Restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @commands.hybrid_command()
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        try:
            await self.bot.load_extension(f"commands.{extension}")

            await ctx.send(f"-# Successfully Loaded **{extension}**")
            print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Loaded {extension}")

        except Exception as e:
            await self.extension_error(ctx, extension, e)

    @commands.hybrid_command()
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        try:
            await self.bot.unload_extension(f"commands.{extension}")

            await ctx.send(f"-# Successfully Unloaded **{extension}**")
            print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Unloaded {extension}")

        except Exception as e:
            await self.extension_error(ctx, extension, e)

    @commands.hybrid_command()
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        try:
            await self.bot.reload_extension(f"commands.{extension}")

            await ctx.send(f"-# Successfully Reloaded **{extension}**")
            print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Reloaded {extension}")

        except Exception as e:
            await self.extension_error(ctx, extension, e)

    @commands.hybrid_command()
    @commands.is_owner()
    async def reloadall(self, ctx):
        ok = []
        failed = []

        for file in (ROOT/"commands").glob("*.py"):
            if file.stem.startswith("_"):
                continue

            ext = f"commands.{file.stem}"

            try:
                await self.bot.reload_extension(ext)
                ok.append(file.stem)
            except Exception as e:
                failed.append(file.stem)
                await self.extension_error(ctx, file.stem, e)

        msg = ""

        if ok:
            msg += f"-# Successfully Reloaded **{len(ok)}** cogs: **{'**, **'.join(ok)}**"

        if ok and failed:
            msg += "\n"

        if failed:
            msg += f"-# Failed on {len(failed)}: **{', '.join(failed)}**"

        await ctx.send(msg)
        print(Style.BRIGHT + Fore.MAGENTA + "[DEV] Reloaded all Cogs")

    @commands.hybrid_command()
    @commands.is_owner()
    async def sync(self, ctx):
        try:
            synced = await self.bot.tree.sync()
            print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Synced {len(synced)} Commands")
            await ctx.send(f"-# Successfully synced {len(synced)} commands")

        except Exception as e:
            print(Style.BRIGHT + Fore.RED + "[ERR] Failed to Sync Commands")
            await ctx.send("-# Failed to Sync Commands")

    @commands.hybrid_command()
    @commands.is_owner()
    async def extensions(self, ctx):
        loaded = sorted(
            ext.removeprefix("commands.")
            for ext in self.bot.extensions
        )

        if not loaded:
            return await ctx.send("-# No Extensions Loaded")

        await ctx.send(f"-# **{len(loaded)}**: **{'**, **'.join(loaded)}**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def logs(self, ctx, log: str, lines: commands.Range[int, 1, 500] = 50):
        logs = {
            p.stem: p
            for p in (ROOT/"logs").glob("*.log")
        }

        path = logs.get(log.lower())

        if path is None:
            return await ctx.send("-# Available Logs: `sys`, `err`")

        try:
            with path.open("r", encoding = "utf-8") as f:
                text = "".join(f.readlines()[-lines:])

            if not text:
                text = "-# File is Empty."

            if len(text) > 1900:
                text = text[-1900:]

            await ctx.send(f"```log\n{text}\n```")

        except FileNotFoundError:
            await ctx.send("-# File not Found")

    async def extension_error(self, ctx, extension, error):
        if isinstance(error, commands.ExtensionNotFound):
            return await ctx.send(f"-# **{extension}** Was Not Found")

        if isinstance(error, commands.ExtensionNotLoaded):
            return await ctx.send(f"-# **{extension}** is Not Loaded")

        if isinstance(error, commands.ExtensionAlreadyLoaded):
            return await ctx.send(f"-# **{extension}** is Already Loaded")

        raise error

async def setup(bot):
    await bot.add_cog(System(bot))
