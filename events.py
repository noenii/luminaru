import discord, time, traceback

from discord.ext import commands
from datetime import datetime, timezone

from helpers.funcs import send
from helpers.handlers import ERROR_HANDLERS
from setup.config import ERROR, WARNING

def register_events(bot):

    @bot.event
    async def on_ready():
        if bot.ready:
            return

        bot.ready = True

        await bot.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="/aki"
            )
        )
        print(
            "=========================================\n\n"
            "      _           _                 \n"
            "     | |_ _ _____|_|___ ___ ___ _ _ \n"
            "     | | | |     | |   | .'|  _| | |\n"
            "     |_|___|_|_|_|_|_|_|__,|_| |___|\n\n"
            "               a cool bot?\n\n"
            "=========================================\n\n"
            f"Successfully logged in as {bot.user} at {datetime.fromtimestamp(time.time(), timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
            "Thank you for hosting!\n\n"
            "=========================================\n"
        )

        bot.system_logger.info("Bot Started Up")
        psutil.cpu_percent(interval=None)

        bot.tree.copy_global_to(guild=1316723730717868093)
        await bot.tree.sync()

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        await bot.process_commands(message)

    @bot.event
    async def on_command_completion(ctx):
        msg = f"Command: {ctx.command}, Requested by: {ctx.author}, Channel: {ctx.channel}"
        bot.command_logger.info(msg)
        print(msg)

    @bot.event
    async def on_command_error(ctx, error):
        error = getattr(error, "original", error)

        handler = ERROR_HANDLERS.get(type(error))

        if handler:
            return await handler(ctx, error)

        await send(
            ctx,
            f"{ERROR}  500! Internal Error! >:(",
            "Something went wrong internally. The devs have been notified!",
            WARNING,
            footer=False
        )

        log_msg = (f"Command: {ctx.command}, Requested by: {ctx.author} ({ctx.author.id}), Channel: {ctx.channel} ({ctx.channel.id}), Message: {ctx.message.content}, Type: {type(error).__name__}: {error}")

        bot.system_logger.error(log_msg)
        bot.error_logger.error(log_msg)
        print(log_msg)
        traceback.print_exception(type(error), error, error.__traceback__)
