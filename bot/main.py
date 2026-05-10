import asyncio, discord, time, threading

from discord.ext import commands

from setup.config import TOKEN, PREFIX
from helpers.funcs import setup_logging
from cogs.commands import register_commands
from events import register_events

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

bot.ready = False
bot.start_time = time.time()

bot.system_logger, bot.command_logger, bot.error_logger = setup_logging()

def console_listener():
    while True:
        cmd = input().lower().strip()

        if cmd == "quit":
            if bot.loop.is_running():
                bot.system_logger.info("Bot Shutdown"),
                asyncio.run_coroutine_threadsafe(
                    bot.close(),
                    bot.loop
                )

            time.sleep(1)
            print("\nShutdown successful.")
            break

async def main():
    register_commands(bot)      # only prefixes rn, slash cmds later
    register_events(bot)

    threading.Thread(target=console_listener, daemon=True).start()

    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
