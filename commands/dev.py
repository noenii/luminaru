import asyncio, os, sys, traceback

from pathlib import Path
from discord.ext import commands

from stuff.funcs import embed, send
from setup.config import SUCCESS, WARNING, ROOT

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await send(ctx, "-# ok bro")
        self.log_command(ctx)

        async def close():
            await asyncio.sleep(0)
            await self.bot.close()

        asyncio.create_task(close())

    @commands.hybrid_command()
    @commands.is_owner()
    async def restart(self, ctx):
        await send(ctx, "-# restarting... gimme a sec")
        self.log_command(ctx)
        print("restarting...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @commands.hybrid_command()
    @commands.is_owner()
    async def load(self, ctx, extension: str):
        try:
            await self.bot.load_extension(f"commands.{extension}")
            await send(ctx, f"-# successfully loaded **{extension}**")
            self.log_command(ctx)
        except Exception as e:
            await self.extension_error(ctx, extension, "load", e)

    @commands.hybrid_command()
    @commands.is_owner()
    async def unload(self, ctx, extension: str):
        try:
            await self.bot.unload_extension(f"commands.{extension}")
            await send(ctx, f"-# successfully unloaded **{extension}**")
            self.log_command(ctx)
        except Exception as e:
            await self.extension_error(ctx, extension, "unload", e)

    @commands.hybrid_command()
    @commands.is_owner()
    async def reload(self, ctx, extension: str):
        try:
            await self.bot.reload_extension(f"commands.{extension}")
            await send(ctx, f"-# successfully reloaded **{extension}**")
            self.log_command(ctx)
        except Exception as e:
            await self.extension_error(ctx, extension, "reload", e)

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
                await self.extension_error(ctx, file.stem, "reload", e)

        msg = ""
        emoji = SUCCESS

        if ok:
            msg += f"-# reloaded {len(ok)}: **{', '.join(ok)}**"

        if ok and failed:
            msg += "\n"

        if failed:
            emoji = WARNING
            msg += f"-# failed on {len(failed)}: **{', '.join(failed)}**"

        await send(ctx, msg, emoji)
        self.log_command(ctx)

    @commands.hybrid_command()
    @commands.is_owner()
    async def sync(self, ctx):
        try:
            synced = await self.bot.tree.sync()
            await send(ctx, f"-# successfully synced {len(synced)} command{'s' if len(synced) != 1 else ''}")
            self.log_command(ctx)

        except Exception as e:
            await send(ctx, "-# failed to sync commands", WARNING)
            self.log_error(ctx, e)

            traceback.print_exception(type(e), e, e.__traceback__)

    @commands.hybrid_command()
    @commands.is_owner()
    async def extensions(self, ctx):
        loaded = sorted(
            ext.removeprefix("commands.")
            for ext in self.bot.extensions
        )

        self.log_command(ctx)

        if not loaded:
            return await send(ctx, "-# no extensions loaded", WARNING)

        await send(ctx, f"-# {len(loaded)}: **{', '.join(loaded)}**")

    @commands.hybrid_command()
    @commands.is_owner()
    async def logs(self, ctx, log: str, lines: commands.Range[int, 1, 500] = 50):
        logs = {
            p.stem: p
            for p in (ROOT/"logs").glob("*.log")
        }

        path = logs.get(log.lower())

        self.log_command(ctx)

        if path is None:
            return await send(ctx, "-# available logs: `system`, `commands`, `errors`, `dev`", WARNING)

        try:
            with path.open("r", encoding = "utf-8") as f:
                text = "".join(f.readlines()[-lines:])

            if not text:
                text = "-# file is empty."

            if len(text) > 1900:
                text = text[-1900:]

            await send(ctx, f"```log\n{text}\n```")

        except FileNotFoundError:
            await send(ctx, "-# file not found", WARNING)

    def log_command(self, ctx):
        self.bot.dev_logger.info(f"Command: {ctx.command}, Requested by: {ctx.author}, Channel: {ctx.channel}")

    def log_error(self, ctx, error):
        msg = (f"Command: {ctx.command}, Requested by: {ctx.author} ({ctx.author.id}), Channel: {ctx.channel} ({ctx.channel.id}), Message: {ctx.message.content}, Type: {type(error).__name__}: {error}")

        self.bot.system_logger.error(msg)
        self.bot.error_logger.error(msg)

    async def extension_error(self, ctx, extension, action, error):
        self.log_error(ctx, error)

        if isinstance(error, commands.ExtensionNotFound):
            return await send(ctx, f"-# **{extension}** wasnt found", WARNING)

        if isinstance(error, commands.ExtensionNotLoaded):
            return await send(ctx, f"-# **{extension}** isnt loaded", WARNING)

        if isinstance(error, commands.ExtensionAlreadyLoaded):
            return await send(ctx, f"-# **{extension}** is already loaded", WARNING)

        if isinstance(error, commands.ExtensionFailed):
            await send(ctx, f"-# failed to {action} **{extension}**", WARNING)

            traceback.print_exception(
                type(error.original),
                error.original,
                error.original.__traceback__
            )

            return

        raise error

async def setup(bot):
    await bot.add_cog(Dev(bot))
