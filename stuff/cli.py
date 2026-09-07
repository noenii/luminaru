import discord, psutil, platform, asyncio, os, colorama, time, sys

from setup.config import ROOT
from stuff.funcs import fmt_time

from colorama import Fore, Style

colorama.init(autoreset = True)

def console_listener(bot, loop):
    while not bot.is_closed():
        try:
            cmd = input().lower().strip()
        except (EOFError, KeyboardInterrupt):
            break

        match cmd:
            case "ping":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] WS: {round(bot.latency * 1000)}")

            case "sys":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] CPU: {psutil.cpu_percent(interval = 0.1):.1f}%, RAM: {psutil.virtual_memory().percent}%")

            case "env":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] PY: {platform.python_version()}, DPY: {discord.__version__}, OS: {platform.system()} {platform.release()} {platform.machine()}")

            case "uptime":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] {fmt_time(int(time.time() - bot.start_time))}")

            case "extensions":
                loaded = sorted(ext.removeprefix("commands.") for ext in bot.extensions)

                if not loaded:
                    print(Fore.YELLOW + "[WRN] No Extensions Loaded")

                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] {len(loaded)}: {', '.join(loaded)}")

            case "sync":
                try:
                    future = asyncio.run_coroutine_threadsafe(bot.tree.sync(), loop)
                    synced = future.result()
                    print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Synced {len(synced)} Commands")
                except Exception as e:
                    print(Fore.YELLOW + "[WRN] Failed to Sync Commands")
                    print(e)

            case "reloadall":
                y = 0
                n = 0

                for file in (ROOT/"commands").glob("*.py"):
                    if file.stem.startswith("_"):
                        continue
                    try:
                        asyncio.run_coroutine_threadsafe(bot.reload_extension(f"commands.{file.stem}"), loop)
                        y += 1
                    except Exception as e:
                        n += 1

                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Reloaded all Cogs ({y-n}/{y})")

            case "quit":
                try:
                    print(Style.BRIGHT + Fore.MAGENTA + "[DEV] Bot Shutdown")
                    bot.system_logger.info("[DEV] Bot Shutdown")
                    asyncio.run_coroutine_threadsafe(bot.close(), loop)
                    break
                except Exception as e:
                    print(Fore.RED + f"[ERR] Error during shutdown: {e}")
                    bot.error_logger.error(f"[ERR] Error during shutdown: {e}")
                    break

            case "restart":
                try:
                    print(Style.BRIGHT + Fore.MAGENTA + "[DEV] Bot Restarting...")
                    bot.system_logger.info("[DEV] Bot Restarting...")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                except Exception as e:
                    print(Fore.RED + f"[ERR] Error During Shutdown: {e}")
                    bot.error_logger.error(f"[ERR] Error During Restart: {e}")
                    break
