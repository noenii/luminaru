import discord, logging, os, time

from datetime import datetime, timezone
from discord.ui import LayoutView

from setup.config import EMBED_COLOR, SUCCESS, DEV, IMP_ROLES

def setup_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    log_dir = os.path.join(project_root, "logs")

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

def embed(ctx, title = None, desc = None, c = EMBED_COLOR):      # to delete
    e = discord.Embed(
        title = title,
        description = desc,
        color = c
    )

    return e

def container(text: str) -> discord.ui.LayoutView:
    view = discord.ui.LayoutView()

    view.add_item(
        discord.ui.Container(
            discord.ui.TextDisplay(text)
        )
    )

    return view

async def send(ctx, i = None, emoji = SUCCESS):
    try:
        if isinstance(i, discord.Embed):
            await ctx.reply(embed = i, mention_author = False)

        elif isinstance(i, discord.ui.View):
            await ctx.reply(view = i, mention_author = False)

        elif isinstance(i, str):
            await ctx.reply(i, mention_author = False)

        if ctx.message:
            try:
                await ctx.message.add_reaction(emoji)
            except (discord.HTTPException, discord.Forbidden):
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

def fmt_date(timestamp: float) -> str:
    dt = datetime.fromtimestamp(timestamp, tz = timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def fmt_bytes(size: int) -> str:
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
