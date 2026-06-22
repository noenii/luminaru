import discord, time, asyncio

from discord.ext import commands
from datetime import datetime, timedelta, timezone
from stuff.services import member_info
from stuff.funcs import embed, send, fmt_time, ts
from setup.config import SUCCESS, LOADING

class member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "member",
        description = "View Someone's Info",
        help = "View Member's Info",
    )
    async def member(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        e = embed(
            ctx,
            "Member Info",
            f"> Name: `{m['name']}`\n"
            f"> User: `{m['username']}`\n"
            f"> Type: `{m['type']}`"
        )
        e.set_thumbnail(url = m['avatar'])

        try:
            await ctx.reply(embed = e, mention_author = False)
            try:
                await ctx.message.add_reaction(SUCCESS)
            except discord.HTTPException:
                pass

        except Exception as e:
            print("SEND ERROR:", type(e).__name__, e)

    @commands.hybrid_command(
        name = "avatar",
        description = "View Someone's Avatar",
        help = "View Member's Avatar"
    )
    async def avatar(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        e = embed(ctx, f"Member Avatar")
        e.set_image(url = m['avatar'])

        try:
            await ctx.reply(embed = e, mention_author = False)
            try:
                await ctx.message.add_reaction(SUCCESS)
            except discord.HTTPException:
                pass

        except Exception as e:
            print("SEND ERROR:", type(e).__name__, e)

    @commands.hybrid_command(
        name = "id",
        description = "View Someone's ID",
        help = "View Member's ID"
    )
    async def id(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        await send(
            ctx,
            "Member ID",
            f"> ID: `{m['id']}`"
        )

    @commands.hybrid_command(
        name = "history",
        description = "View Someone's History",
        help = "View Member's History"
    )
    async def history(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        await send(
            ctx,
            "Member History",
            f"> Joined: {ts(int(m['joined'].timestamp()), 'R')}\n"
            f"> Created: {ts(int(m['created'].timestamp()), 'R')}\n"
        )

    @commands.hybrid_command(
        name = "status",
        description = "View Someone's Status",
        help = "View Member's Status"
    )
    async def status(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        await send(
            ctx,
            "`Member Status",
            f"{m['status']}\n"
            f"{m['activity']}"
        )

    @commands.hybrid_command(
        name = "boost",
        description = "View Booster Stats",
        help = "View Member's Boosting Stats"
    )
    async def status(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)
        boosting = "> Boosting: `False`"
        if m['boost']:
            boosting = f"> Boosting: `True`\n> Since: {ts(int(m['boost_d'].timestamp()), 'R')}"

        await send(
            ctx,
            "Boosting Stats",
            f"{boosting}"
        )

    @commands.hybrid_command(
        name = "roles",
        description = "View Member's Roles",
        help = "Displays a Member's Roles"
    )
    async def roles(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        await send(
            ctx,
            "Member Roles",
            f"{m['roles']}"
        )

    @commands.hybrid_command(
        name = "perms",
        description = "View Member's Permissions",
        help = "View Member's Permissions"
    )
    async def perms(self, ctx: commands.Context,  member: discord.Member = None):
        member = member or ctx.author
        m = member_info(ctx, member)

        await send(
            ctx,
            "Member Perms",
            f"`{m['perms']}`"
        )

async def setup(bot):
    await bot.add_cog(member(bot))
