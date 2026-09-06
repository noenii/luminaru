import asyncio, discord, time, threading, os, sys, colorama

from discord.ext import commands
from colorama import Fore, Style

from setup.config import TOKEN, PREFIX, ROOT
from stuff.funcs import setup_logging

from events import register_events

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix = PREFIX, intents = intents)

bot.ready = False
bot.start_time = time.time()

bot.system_logger, bot.error_logger = setup_logging()
colorama.init(autoreset = True)

def console_listener(loop):
    while not bot.is_closed():
        try:
            cmd = input().lower().strip()
        except (EOFError, KeyboardInterrupt):
            break

        if cmd == "quit":
            try:
                print(Style.BRIGHT + Fore.BLUE + "[SYS] Bot Shutdown")
                bot.system_logger.info("[SYS] Bot Shutdown")
                asyncio.run_coroutine_threadsafe(bot.close(), loop)
                break
            except Exception as e:
                print(Fore.RED + f"[ERR] Error during shutdown: {e}")
                bot.error_logger.error(f"[ERR] Error during shutdown: {e}")
                break

async def main():
    print(Style.BRIGHT + Fore.BLUE + "[SYS] Starting up...")

    extension_dir = os.path.join(ROOT, "commands")
    if os.path.exists(extension_dir):
        filez = [f for f in os.listdir(extension_dir) if f.endswith(".py") and not f.startswith("_")]
    else:
        filez = []

    tf = len(filez)
    fe = []

    print(Style.BRIGHT + Fore.BLUE + "[SYS] Loading Extensions...\n")

    for fn in filez:
        print(Style.BRIGHT + Fore.BLUE + f"[SYS] Loading: {fn}")

        try:
            await bot.load_extension(f"commands.{fn[:-3]}")
        except Exception as e:
            print(Style.BRIGHT + Fore.RED + f"[ERR] {e}")
            bot.error_logger.error(f"[ERR] Failed to load extension {fn}, Error: {e}")
            fe.append(fn)

    print(Style.BRIGHT + Fore.BLUE + f"\n[SYS] Successfully Loaded Extensions ({tf - len(fe)}/{tf})")

    if fe:
        failed_str = ", ".join(fe)
        print(Style.BRIGHT + Fore.YELLOW + f"[WRN] Failed to Load: {failed_str}")

    register_events(bot)

    loop = asyncio.get_running_loop()
    threading.Thread(target = console_listener, args = (loop,), daemon = True).start()

    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Style.BRIGHT + Fore.BLUE + "\n[SYS] Bot Shutdown")
        bot.system_logger.info("[SYS] Bot Shutdown")
