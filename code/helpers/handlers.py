import difflib
from discord.ext import commands

from helpers.funcs import send
from setup.config import ERROR, WARNING

# Note to self: ctx means context
async def handle_command_not_found(ctx, error):
    commands = [cmd.name for cmd in ctx.bot.commands]

    closeMatches = difflib.get_close_matches(ctx.invoked_with, commands, n=3, cutoff=0.7)

    s = ("\n".join(f"`{i}`" for i in closeMatches) if closeMatches else "No similar commands found.")

    return await send(
        ctx,
        f"{ERROR}  404! Command Not Found! >:(",
        f"The command does not exist or was typed incorrectly!\n> Closest Command/s: {s}",
        WARNING
    )

async def handle_missing_required_argument(ctx, error):
    u = (
        f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    return await send(
        ctx,
        f"{ERROR}  400! Missing Required Argument(s)! >:(",
        f"Missing Required Argument/s!\n> Correct Usage: `{u}`",
        WARNING
    )

async def handle_bad_argument(ctx, error):
    u = (f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    return await send(
        ctx,
        f"{ERROR}  400! Invalid Arg/Args >:(",
        f"Invalid Argument/s!\n> Details: `{error}`\n> Usage: `{u}`",
        WARNING
    )

async def handle_missing_permissions(ctx, error):
    p = ", ".join(p.replace("_", " ").title() for p in error.missing_permissions)

    return await send(
        ctx,
        f"{ERROR}  403! You can't use this command! >:(",
        f"You are missing permissions to use this command!\n> Permission/s: `{p}`",
        WARNING
    )

async def handle_missing_role(ctx, error):
    return await send(
        ctx,
        f"{ERROR}  403! Missing Role! >:(",
        f"You don't have a required role!\n> Role: `{error.missing_role}`",
        WARNING
    )

async def handle_missing_any_role(ctx, error):
    r = ", ".join(error.missing_roles)

    return await send(
        ctx,
        f"{ERROR}  403! Missing Roles! >:(",
        f"You don't have the required roles!\n> Roles: `{r}`",
        WARNING
    )

async def handle_command_on_cooldown(ctx, error):
    return await send(
        ctx,
        f"{ERROR}  429! Too Many Requests! >:(",
        f"Cooldown flagged!\n> Try again in: `{round(error.retry_after, 1)}s`",
        WARNING
    )

ERROR_HANDLERS = {
    commands.CommandNotFound: handle_command_not_found,
    commands.MissingRequiredArgument: handle_missing_required_argument,
    commands.BadArgument: handle_bad_argument,
    commands.MissingPermissions: handle_missing_permissions,
    commands.MissingRole: handle_missing_role,
    commands.MissingAnyRole: handle_missing_any_role,
    commands.CommandOnCooldown: handle_command_on_cooldown,
}
