import discord, difflib
from discord.ext import commands

async def handle_command_not_found(ctx, error):
    c = [cmd.name for cmd in ctx.bot.commands]
    m = difflib.get_close_matches(ctx.invoked_with, c, n = 3, cutoff = 0.7)
    s = ("\n".join(f"`{i}`" for i in m) if m else "No similar commands found.")

    e = discord.Embed(
        title = f"404: Command Not Found",
        description = f"The command does not exist or was typed incorrectly.\n> Closest: {s}"
    )

    return await ctx.send(embed = e)

async def handle_missing_required_argument(ctx, error):
    u = (f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    e = discord.Embed(
        title = f"400: Missing Required Argument",
        description = f"Missing Required Argument.\n> Usage: `{u}`"
    )

    return await ctx.send(embed = e)

async def handle_bad_argument(ctx, error):
    u = (f"{ctx.prefix}{ctx.command.qualified_name} {' '.join(f'<{p}>' for p in ctx.command.clean_params)}")

    e = discord.Embed(
        title = f"400: Invalid Argument",
        description = f"Invalid Argument.\n> Details: `{error}`\n> Usage: `{u}`"
    )

    return await ctx.send(embed = e)

async def handle_missing_permissions(ctx, error):
    p = ", ".join(p.replace("_", " ").title() for p in error.missing_permissions)

    e = discord.Embed(
        title = f"403: You can\'t use this command",
        description = f"You are missing permissions to use this command.\n> Permissions: `{p}`"
    )

    return await ctx.send(embed = e)

async def handle_missing_role(ctx, error):
    e = discord.Embed(
        title = f"403: Missing Role",
        description = f"You don't have a required role.\n> Role: `{error.missing_role}`"
    )

    return await send(ctx, e)

async def handle_missing_any_role(ctx, error):
    r = ", ".join(error.missing_roles)

    e = discord.Embed(
        title = f"403: Missing Roles",
        description = f"You don't have the required roles.\n> Roles: `{r}`"
    )

    return await ctx.send(embed = e)

async def handle_command_on_cooldown(ctx, error):
    e = discord.Embed(
        title = f"429: Too Many Requests",
        description = f"Cooldown flagged.\n> Try again in: `{round(error.retry_after, 1)}s`"
    )

    return await ctx.send(embed = e)

ERROR_HANDLERS = {
    commands.CommandNotFound: handle_command_not_found,
    commands.MissingRequiredArgument: handle_missing_required_argument,
    commands.BadArgument: handle_bad_argument,
    commands.MissingPermissions: handle_missing_permissions,
    commands.MissingRole: handle_missing_role,
    commands.MissingAnyRole: handle_missing_any_role,
    commands.CommandOnCooldown: handle_command_on_cooldown,
}
