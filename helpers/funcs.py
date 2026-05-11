import discord, logging, os, time

from datetime import datetime, timezone

from setup.config import EMBED_COLOR, SUCCESS, STAFF

def setup_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    log_dir = os.path.join(project_root, "logs")

    os.makedirs(log_dir, exist_ok=True)

    fmt = logging.Formatter("%(levelname)s - %(message)s - %(asctime)s")

    def build_logger(name, filename, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)

        if not logger.handlers:
            file_path = os.path.join(log_dir, filename)

            handler = logging.FileHandler(file_path, encoding="utf-8")
            handler.setFormatter(fmt)
            logger.addHandler(handler)

        return logger

    system_logger = build_logger("system", "system.log", logging.INFO)
    command_logger = build_logger("commands", "commands.log", logging.INFO)
    error_logger = build_logger("errors", "errors.log", logging.ERROR)

    return system_logger, command_logger, error_logger

def embed(ctx, title=None, desc=None, icon=False, footer=False):
    e = discord.Embed(
        title=title,
        description=desc,
        color=EMBED_COLOR
    )
    if icon:
        if ctx.guild:
            e.set_author(
                name=ctx.guild.name,
                icon_url=ctx.guild.icon.url if ctx.guild.icon else None
            )
    if footer:
        e.set_footer(text=f"Requested by {ctx.author}")

    return e

async def send(ctx, title=None, desc=None, emoji=SUCCESS, icon=False, footer=False):
    try:
        await ctx.reply(embed=embed(ctx, title, desc, icon, footer), mention_author=False)

        try:
            await ctx.message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    except Exception as e:
        print("SEND ERROR:", type(e).__name__, e)

def online(guild):
    return sum(m.status != discord.Status.offline for m in guild.members)

def is_staff(ctx):
    return any(r.name in STAFF for r in ctx.author.roles)

def ts(t):
    return f"<t:{int(t.timestamp())}:F>"

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
