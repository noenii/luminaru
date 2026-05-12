import discord, psutil, platform, sys, time

from datetime import datetime, timezone

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

    sent_mb = net.bytes_sent
    received_mb = net.bytes_recv

    ping = round(bot.latency * 1000)

    system_start = psutil.boot_time()

    return {
        "cpu": cpu_usage, "cores": cores, "threads": threads,
        "ram": ram_used, "ram_pct": ram_pct, "disk_pct": disk_pct,
        "os": os_name, "vers": os_vers, "arch": os_arch, "py": py_ver, "dpy": dpy_ver,
        "ping": ping, "sent": sent_mb, "recv": received_mb,
        "sys_start": system_start
    }
