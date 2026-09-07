import discord, asyncio, os, platform, sys, time, colorama, psutil, subprocess

from discord.ext import commands
from colorama import Fore, Style

from setup.config import ROOT
from stuff.funcs import fmt_time

colorama.init(autoreset = True)

def extension_error(ex, e):
    if isinstance(e, commands.ExtensionNotFound):
        return f"[WRN] {ex} Was Not Found"
    if isinstance(e, commands.ExtensionNotLoaded):
        return f"[WRN] {ex} is Not Loaded"
    if isinstance(e, commands.ExtensionAlreadyLoaded):
        return f"[WRN] {ex} is Already Loaded"
    return f"[ERR] {e}"

def console_listener(bot, loop):
    while not bot.is_closed():
        try:
            r = input().strip()
            if not r:
                continue
            p = r.split()
            cmd = p[0].lower()
            args = p[1:] if len(p) > 1 else []

        except (EOFError, KeyboardInterrupt):
            break

        match cmd:      # ik its lazy, icba to write decent code
            case "ping":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] WS: {round(bot.latency * 1000)}")

            case "sys":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] CPU: {psutil.cpu_percent(interval = 0.1):.1f}%, RAM: {psutil.virtual_memory().percent}%")

            case "env":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] PY: {platform.python_version()}, DPY: {discord.__version__}, OS: {platform.system()} {platform.release()} {platform.machine()}")

            case "uptime":
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] {fmt_time(int(time.time() - bot.start_time))}")

            case "load":
                if not args:
                    print(Fore.YELLOW + "[WRN] Load What")
                    continue

                for arg in args:
                    try:
                        f = asyncio.run_coroutine_threadsafe(bot.load_extension(f"commands.{arg}"), loop)
                        f.result()
                        print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Loaded {arg}")
                    except Exception as e:
                        print(Fore.YELLOW + extension_error(arg, e))

            case "unload":
                if not args:
                    print(Fore.YELLOW + "[WRN] Unload What")
                    continue

                for arg in args:
                    try:
                        f = asyncio.run_coroutine_threadsafe(bot.unload_extension(f"commands.{arg}"), loop)
                        f.result()
                        print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Unloaded {arg}")
                    except Exception as e:
                        print(Fore.YELLOW + extension_error(arg, e))

            case "reload":
                if not args:
                    print(Fore.YELLOW + "[WRN] Reload What")
                    continue
                for arg in args:
                    try:
                        f = asyncio.run_coroutine_threadsafe(bot.reload_extension(f"commands.{arg}"), loop)
                        f.result()
                        print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Reloaded {arg}")
                    except Exception as e:
                        print(Fore.YELLOW + extension_error(arg, e))

            case "reloadall":
                y = 0
                n = 0
                for file in (ROOT / "commands").glob("*.py"):
                    if file.stem.startswith("_"):
                        continue
                    try:
                        asyncio.run_coroutine_threadsafe(bot.reload_extension(f"commands.{file.stem}"), loop).result()
                        y += 1
                    except Exception as e:
                        n += 1
                        print(Fore.RED + f"[ERR] Failed to Reload Modules {file.stem}: {e}")
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Reloaded Modules ({y}/{y + n})")

            case "extensions":
                loaded = sorted(ext.removeprefix("commands.") for ext in bot.extensions)
                if not loaded:
                    print(Fore.YELLOW + "[WRN] No Extensions Loaded")
                    continue
                print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] {len(loaded)}: {', '.join(loaded)}")

            case "sync":
                try:
                    f = asyncio.run_coroutine_threadsafe(bot.tree.sync(), loop)
                    s = f.result()
                    print(Style.BRIGHT + Fore.MAGENTA + f"[DEV] Synced {len(s)} Commands")
                except Exception as e:
                    print(Fore.YELLOW + "[WRN] Failed to Sync Commands")

            case "logs":
                if len(args) < 2:
                    print(Fore.YELLOW + "[WRN] Correct Usage: logs <file> <int>")
                    continue

                log_name = args[0].lower()

                try:
                    lines = int(args[1])
                    if lines <= 0:
                        raise ValueError
                except ValueError:
                    print(Fore.YELLOW + "[WRN] Enter a Positive Integer")
                    continue

                logs = {
                    p.stem.lower(): p
                    for p in (ROOT / "logs").glob("*.log")
                }

                path = logs.get(log_name)

                if path is None:
                    available = ", ".join(f"{k}" for k in logs.keys()) if logs else "Logs Unavailable"
                    print(Fore.YELLOW + f"[WRN] Available Logs: {available}")
                    continue

                try:
                    with path.open("r", encoding = "utf-8") as f:
                        all_lines = f.readlines()
                        text = "".join(all_lines[-lines:])

                    if not text:
                        print(Fore.YELLOW + "[WRN] File is Empty")
                        continue

                    if len(text) > 1900:
                        text = text[-1900:]

                    print(Style.BRIGHT + Fore.MAGENTA + f"\n[DEV] {log_name}.log\n")
                    print(Style.DIM + Fore.BLUE + text + "\n")

                except FileNotFoundError:
                    print(Fore.RED + "[ERR] File was not Found")

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
                    print(e)

            case "help":
                if not args:
                    print(Style.BRIGHT + Fore.GREEN + "[AKI] Commands List: [list]\n[AKI] Command Help: [help <command>]\n[AKI] External Links: [links]")
                    continue
                match args[0].lower():
                    case "ping":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Displays Ping in MS")
                    case "sys":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Displays CPU And RAM Stats")
                    case "env":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Displays Enviroment Info")
                    case "uptime":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] View Uptime")
                    case "load":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Loads Extension [load <list>]")
                    case "unload":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Unloads Extension [unload <list>]")
                    case "reload":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Reloads Extension [reload <list>]")
                    case "reloadall":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Reload All Extensions")
                    case "extensions":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] View Loaded Extensions")
                    case "sync":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Sync Commands")
                    case "logs":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] View Logs [logs <log> <int>]")
                    case "quit":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Shuts Down The Bot")
                    case "restart":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Restarts The Bot (this one breaks the cli tho)")
                    case "help":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Help Command")
                    case "list":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Displays All CLI Commands")
                    case "links":
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Displays External Links For This Bot")
                    case _:
                        print(Style.BRIGHT + Fore.GREEN + "[AKI] Unknown Command")
                continue

            case "list":
                print(Style.BRIGHT + Fore.GREEN + "[AKI] Commands: ping, sys, env, uptime, load, unload, reload, reloadall, extensions, sync, logs, quit, restart")
                continue

            case "links":
                print(Style.BRIGHT + Fore.GREEN + "[AKI] Github: https://github.com/noenii/lumi\n[AKI] Discord: https://discord.gg/yqWZyrh3wW")
                continue
