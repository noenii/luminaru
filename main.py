import asyncio, discord, time, threading, os

from discord.ext import commands

from setup.config import TOKEN, PREFIX
from helpers.funcs import setup_logging

from events import register_events

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

bot.ready = False
bot.start_time = time.time()

bot.system_logger, bot.command_logger, bot.error_logger = setup_logging()

def console_listener():
    while True:
        cmd = input().lower().strip()
        if cmd == "quit":
            future = asyncio.run_coroutine_threadsafe(bot.close(), bot.loop)
            try:
                future.result(timeout=10)
            except Exception as e:
                print(f"Error during shutdown: {e}")
            bot.system_logger.info("Bot Shutdown")
            print("\nShutdown successful.")
            break

async def main():

    for filename in os.listdir('bot/commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')   # only prefixes rn, slash cmds later
                bot.system_logger.info(f"Loaded extension: {filename}")
            except Exception as e:
                err = f"Failed to load extension: {filename} - {e}"
                print(err)
                bot.error_logger.error(err)

    register_events(bot)

    threading.Thread(target=console_listener, daemon=True).start()

    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
