import discord, logging, os

from datetime import datetime, timezone
from discord.ui import LayoutView

from setup.config import ROOT, EMBED_COLOR

def setup_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    log_dir = ROOT/"logs"

    os.makedirs(log_dir, exist_ok = True)

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    def build_logger(name, filename, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            file_path = os.path.join(log_dir, filename)

            handler = logging.FileHandler(file_path, encoding = "utf-8")
            handler.setFormatter(fmt)
            logger.addHandler(handler)

        return logger

    system_logger = build_logger("system", "system.log", logging.INFO)
    command_logger = build_logger("commands", "commands.log", logging.INFO)
    error_logger = build_logger("errors", "errors.log", logging.ERROR)
    dev_logger = build_logger("dev", "dev.log", logging.INFO)

    return system_logger, command_logger, error_logger, dev_logger

def embed(ctx, title = None, desc = None, c = EMBED_COLOR):
    e = discord.Embed(
        title = title,
        description = desc,
        color = c
    )

    return e

def container(text: str):
    view = discord.ui.LayoutView()

    view.add_item(
        discord.ui.Container(
            discord.ui.TextDisplay(text)
        )
    )

    return view

async def send(ctx, i = None):
    try:
        if isinstance(i, discord.Embed):
            await ctx.send(embed = i)

        elif isinstance(i, discord.ui.View):
            await ctx.send(view = i)

        elif isinstance(i, str):
            await ctx.send(i)

    except Exception as e:
        print("SEND ERROR:", type(e).__name__, e)

def ts(t, style: str = "R"):
    return f"<t:{int(t)}:{style}>"

def fmt_time(seconds: int):
    intervals = (
        ("y", 31536000),
        ("mo", 2592000),
        ("d", 86400),
        ("h", 3600),
        ("m", 60),
        ("s", 1),
    )

    parts = []

    for name, amount in intervals:
        value, seconds = divmod(seconds, amount)

        if value:
            parts.append(f"{value}{name}")

    return " ".join(parts) or "0s"

def fetch_status(ctx, member: discord.Member = None):
    member = member or ctx.author

    status_map = {
        discord.Status.online: "Online",
        discord.Status.idle: "Idle",
        discord.Status.dnd: "DND",
        discord.Status.offline: "Offline",
    }

    status = status_map.get(member.status, "Offline")

    stat = ""
    custom_act = discord.utils.get(
        member.activities, type=discord.ActivityType.custom
    )

    if custom_act:
        status_text = custom_act.state or ""
        emoji_text = f"{custom_act.emoji} " if custom_act.emoji else ""

        if status_text or emoji_text:
            stat = f"{emoji_text}**{status_text}**"

    lines = []
    for act in member.activities:
        if isinstance(act, discord.CustomActivity):
            continue

        if isinstance(act, discord.Game):
            lines.append(f"-# Playing **{act.name}**")

        elif isinstance(act, discord.Streaming):
            lines.append(f"-# Streaming **{act.name}** ({act.platform})")

        elif isinstance(act, discord.Spotify):
            lines.append(f"-# Listening to **{act.title}** by **{act.artist}**")

        elif isinstance(act, discord.Activity):
            if act.type == discord.ActivityType.watching:
                lines.append(f"-# Watching **{act.name}**")
            elif act.type == discord.ActivityType.listening:
                lines.append(f"-# Listening to **{act.name}**")
            elif act.type == discord.ActivityType.playing:
                lines.append(f"-# Playing **{act.name}**")
            elif act.type == discord.ActivityType.competing:
                lines.append(f"-# Competing in **{act.name}**")
            else:
                lines.append(f"-# {act.type.name.title()} **{act.name}**")

    s = f"-# {stat}, **{status}**" if stat else f"-# **{status}**"
    a = "\n".join(lines) if lines else ""

    return s, a

async def joinpos(ctx, member: discord.Member):
    guild = ctx.guild
    if not guild:
        return 0

    if not guild.chunked:
        await guild.chunk()

    sorted_members = sorted(
        [m for m in guild.members if m.joined_at is not None],
        key = lambda m: m.joined_at
    )

    try:
        return sorted_members.index(member) + 1
    except ValueError:
        return 0

def list_roles(ctx, member: discord.Member = None):
    member = member or ctx.author
    f_roles = [r for r in member.roles if not r.is_default()]
    f_roles.sort(key = lambda x: x.position, reverse = True)

    roles = " ".join([r.mention for r in f_roles]) or ""

    return roles

def list_perms(member: discord.Member):
    if member.guild_permissions.administrator:
        return ["Administrator"]

    return [
        perm.replace("_", " ").title()
        for perm, value in member.guild_permissions
        if value
    ]

def perm_check(role: discord.Role):
    p = (
        'administrator',
        'manage_guild',
        'manage_roles',
        'manage_channels',
        'manage_webhooks',
        'manage_expressions',
        'kick_members',
        'ban_members',
        'mention_everyone',
        'moderate_members',
    )

    return any(getattr(role.permissions, flag, False) for flag in p)
