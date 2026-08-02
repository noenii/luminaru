import discord, time, asyncio

from discord.ext import commands
from datetime import datetime, timedelta, timezone
from stuff.funcs import container, send, fmt_time, ts, fetch_mem_info
from setup.config import SUCCESS, LOADING

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''
    broken asl rn ignore
    @commands.hybrid_command(
        name = "member",
        description = "View Someone's Info",
        help = "View Member's Info",
    )
    async def member(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        badges, status, activity = fetch_mem_info(ctx, member)

        ctx,
        f"> Name: `{member.global_name or member.display_name}`\n"
        f"> User: `{member.name}`\n"
        f"> Type: `{badges}`"


    @commands.hybrid_command(
        name = "avatar",
        description = "View Someone's Avatar",
        help = "View Member's Avatar"
    )
    async def avatar(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

    @commands.hybrid_command(
        name = "id",
        description = "View Someone's ID",
        help = "View Member's ID"
    )
    async def id(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        await send(
            ctx,
            f"> ID: `{member.id}`"
        )

    @commands.hybrid_command(
        name = "history",
        description = "View Someone's History",
        help = "View Member's History"
    )
    async def history(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        await send(
            ctx,
            f"> Joined: {ts(int(member.joined_at.timestamp()), 'R')}\n"
            f"> Created: {ts(int(member.created_at.timestamp()), 'R')}\n"
        )

    @commands.hybrid_command(
        name = "status",
        description = "View Someone's Status",
        help = "View Member's Status"
    )
    async def status(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        badges, status, activity = fetch_mem_info(ctx, member)

        await send(
            ctx,
            f"{status}\n"
            f"{activity}"
        )

    @commands.hybrid_command(
        name = "boost",
        description = "View Booster Stats",
        help = "View Member's Boosting Stats"
    )
    async def boost(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        boosting = "> Boosting: `False`"

        if member.premium_since is not None:
            boosting = f"> Boosting: `True`\n> Since: {ts(int(member.premium_since.timestamp()), 'R')}"

        await send(
            ctx,
            f"{boosting}"
        )

    @commands.hybrid_command(
        name = "roles",
        description = "View Member's Roles",
        help = "Displays a Member's Roles"
    )
    async def roles(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        f_roles = [r for r in member.roles if not r.is_default()]
        f_roles.sort(key = lambda x: x.position, reverse = True)

        roles = " ".join([r.mention for r in f_roles]) or "`None`"

        await send(
            ctx,
            f"{roles}"
        )

    @commands.hybrid_command(
        name = "perms",
        description = "View Member's Permissions",
        help = "View Member's Permissions"
    )
    async def perms(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author

        if member.guild_permissions.administrator:
            perms = "`Administrator`"
        else:
            perms = [p[0] for p in member.guild_permissions if p[1]]
            perms = ", ".join(
                p.replace('_', ' ').title() for p in perms
            ) or "None"

        await send(
            ctx,
            f"{perms}"
        )
        '''

async def setup(bot):
    await bot.add_cog(Member(bot))
