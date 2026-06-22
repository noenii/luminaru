import discord, logging, os, time

from datetime import datetime, timezone

from setup.config import EMBED_COLOR, SUCCESS, DEV, IMP_ROLES

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

            handler = logging.FileHandler(file_path, encoding = "utf-8")
            handler.setFormatter(fmt)
            logger.addHandler(handler)

        return logger

    system_logger = build_logger("system", "system.log", logging.INFO)
    command_logger = build_logger("commands", "commands.log", logging.INFO)
    error_logger = build_logger("errors", "errors.log", logging.ERROR)

    return system_logger, command_logger, error_logger

def embed(ctx, title = None, desc = None, footer = True):
    e = discord.Embed(
        title = title,
        description=desc,
        color=EMBED_COLOR
    )
    if footer:
        e.set_footer(text=f"Requested by {ctx.author}")

    return e

async def send(ctx, title = None, desc = None, emoji = SUCCESS, footer = True):
    try:
        await ctx.reply(embed = embed(ctx, title, desc, footer), mention_author = False)
        try:
            await ctx.message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    except Exception as e:
        print("SEND ERROR:", type(e).__name__, e)

def online(guild):
    return sum(m.status != discord.Status.offline for m in guild.members)

def is_dev(ctx):
    return any(r.name in DEV for r in ctx.author.roles)

def ts(t, style: str = "R") -> str:
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

def format_bytes(size: int) -> str:
    units = ['b', 'kb', 'mb', 'gb']

    i = 0

    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1

    return f"{round(size, 2):g} {units[i]}"

def fetch_mem_info(ctx, member: discord.Member) -> tuple[str, str, str]:
    member = member or ctx.author
    badges = []

    member_role_ids = {role.id for role in member.roles}

    role_badge_mapping = {
        "owner": "Owner", "dev": "Dev", "admin": "Admin",
        "mod": "Mod", "pm": "PM", "im": "IM",
        "staff": "Staff", "botp": "Bot+",
        "vip": "VIP", "og": "OG", "pooks": "Pookie"
    }

    for key, badge_name in role_badge_mapping.items():
        role_id = IMP_ROLES.get(key)
        if role_id and role_id in member_role_ids:
            badges.append(badge_name)

    if member.premium_since:
        badges.append("Booster")
    if member.bot:
        badges.append("Bot")
    if not badges:
        badges.append("Member")

    badge_text = ", ".join(badges)

    status_map = {
        discord.Status.online: "`Online`",
        discord.Status.idle: "`Idle`",
        discord.Status.dnd: "`DND`",
        discord.Status.offline: "`Offline`",
    }
    status = status_map.get(member.status, "`N/A`")

    if not member.activities:
        return badge_text, status, "> Activity: `N/A.`"

    lines = []
    for act in member.activities:
        if isinstance(act, discord.Game):
            lines.append(f"> Playing `{act.name}`")

        elif isinstance(act, discord.Streaming):
            lines.append(f"> Streaming `{act.name}` ({act.platform})")

        elif isinstance(act, discord.Spotify):
            lines.append(f"> Listening to `{act.title}` by `{act.artist}`")

        elif isinstance(act, discord.CustomActivity):
            status_text = act.name if act.name else ""
            emoji_text = f"{act.emoji} " if act.emoji else ""
            if status_text or emoji_text:
                status = f"> {emoji_text}`{status_text}`\n> Status: " + status

        elif isinstance(act, discord.Activity):
            if act.type == discord.ActivityType.watching:
                lines.append(f"> Watching `{act.name}`")
            elif act.type == discord.ActivityType.listening:
                lines.append(f"> Listening to `{act.name}`")
            elif act.type == discord.ActivityType.playing:
                lines.append(f"> Playing `{act.name}`")
            else:
                lines.append(f"> {act.type.name.title()} `{act.name}`")
        else:
            lines.append(f"> {str(act)}")

    activity = "\n".join(lines) if lines else "> Activity: `N/A`"
    return badge_text, status, activity
