import difflib
from discord.ext import commands

from stuff.funcs import send, embed

async def handle_command_not_found(ctx, error):
    c = [cmd.name for cmd in ctx.bot.commands]
    m = difflib.get_close_matches(ctx.invoked_with, c, n = 3, cutoff = 0.7)
    s = ("\n".join(f"`{i}`" for i in m) if m else "No similar commands found.")

    e = embed(
        ctx,
        f"404: Command Not Found",
        f"The command does not exist or was typed incorrectly.\n> Closest: {s}",
        0xED4245
    )

    return await send(ctx, e)

async def handle_missing_required_argument(ctx, error):
    u = (f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    e = embed(
        ctx,
        f"400: Missing Required Argument",
        f"Missing Required Argument.\n> Usage: `{u}`",
        0xED4245
    )

    return await send(ctx, e)

async def handle_bad_argument(ctx, error):
    u = (f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    e = embed(
        ctx,
        f"400: Invalid Argument",
        f"Invalid Argument.\n> Details: `{error}`\n> Usage: `{u}`",
        0xED4245
    )

    return await send(ctx, e)

async def handle_missing_permissions(ctx, error):
    p = ", ".join(p.replace("_", " ").title() for p in error.missing_permissions)

    e = embed(
        ctx,
        f"403: You can\'t use this command",
        f"You are missing permissions to use this command.\n> Permissions: `{p}`",
        0xED4245
    )

    return await send(ctx, e)

async def handle_missing_role(ctx, error):
    e = embed(
        ctx,
        f"403: Missing Role",
        f"You don't have a required role.\n> Role: `{error.missing_role}`",
        0xED4245
    )

    return await send(ctx, e)

async def handle_missing_any_role(ctx, error):
    r = ", ".join(error.missing_roles)

    e = embed(
        ctx,
        f"403: Missing Roles",
        f"You don't have the required roles.\n> Roles: `{r}`",
        0xED4245
    )

    return await send(ctx, e)

async def handle_command_on_cooldown(ctx, error):
    e = embed(
        ctx,
        f"429: Too Many Requests",
        f"Cooldown flagged.\n> Try again in: `{round(error.retry_after, 1)}s`",
        0xED4245
    )

    return await send(ctx, e)

ERROR_HANDLERS = {
    commands.CommandNotFound: handle_command_not_found,
    commands.MissingRequiredArgument: handle_missing_required_argument,
    commands.BadArgument: handle_bad_argument,
    commands.MissingPermissions: handle_missing_permissions,
    commands.MissingRole: handle_missing_role,
    commands.MissingAnyRole: handle_missing_any_role,
    commands.CommandOnCooldown: handle_command_on_cooldown,
}
