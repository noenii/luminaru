import discord, psutil, platform, sys, time

from datetime import datetime, timezone
from stuff.funcs import fetch_mem_info

def system_stats(bot, start_time):
    cpu_usage = psutil.cpu_percent(interval=None)
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)

    os_name = platform.system()
    os_vers = platform.release()
    os_arch = platform.machine()

    ram = psutil.virtual_memory()
    ram_used = round(ram.used, 2)
    ram_pct = ram.percent

    disk_pct = psutil.disk_usage('/').percent

    py_ver = platform.python_version()
    dpy_ver = discord.__version__

    net = psutil.net_io_counters(pernic=False)

    sent = net.bytes_sent
    received = net.bytes_recv

    ping = round(bot.latency * 1000)

    system_start = psutil.boot_time()

    return {
        "cpu": cpu_usage, "cores": cores, "threads": threads,
        "ram": ram_used, "ram_pct": ram_pct, "disk_pct": disk_pct,
        "os": os_name, "vers": os_vers, "arch": os_arch, "py": py_ver, "dpy": dpy_ver,
        "ping": ping, "sent": sent, "recv": received,
        "sys_start": system_start
    }

def member_info(ctx, member: discord.Member) -> dict:
    guild = ctx.guild
    badges, status, activity = fetch_mem_info(ctx, member)

    name = member.global_name or member.display_name

    joined = member.joined_at
    created = member.created_at

    boost = member.premium_since is not None
    boost_d = member.premium_since

    f_roles = [r for r in member.roles if not r.is_default()]

    f_roles.sort(key = lambda x: x.position, reverse = True)

    roles = " ".join([r.mention for r in f_roles]) or "`None`"

    if member.guild_permissions.administrator:
        perms = "`Administrator`"
    else:
        perms = [p[0] for p in member.guild_permissions if p[1]]
        perms = ", ".join(
            p.replace('_', ' ').title() for p in perms
        ) or "None"

    voice = "`N/A`"
    if member.voice and member.voice.channel:
        voice = f"In: `{member.voice.channel.name}`"

    return {
        "name": name, "username": member.name, "type": badges, "id": member.id,
        "avatar": member.display_avatar.url,
        "joined": joined, "created": created,
        "status": status, "activity": activity,
        "boost": boost, "boost_d": boost_d,
        "roles": roles, "perms": perms,
        "voice": voice,
    }
