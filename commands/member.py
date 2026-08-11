import discord, time, asyncio

from discord.ext import commands
from datetime import datetime, timedelta, timezone
from stuff.funcs import embed, send, fmt_time, ts, fetch_status, joinpos, list_roles, list_perms
from stuff.views import paginate, send_pages
from setup.config import SUCCESS, LOADING

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def member(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        e = embed(ctx, "", "")

        e.add_field(
            name = "joined",
            value = f"> <t:{int(member.joined_at.timestamp())}:D> (<t:{int(member.joined_at.timestamp())}:R>)",
            inline = False
        )

        e.add_field(
            name = "created",
            value = f"> <t:{int(member.created_at.timestamp())}:D> (<t:{int(member.created_at.timestamp())}:R>)",
            inline = False
        )

        e.add_field(
            name = f"roles ({len(member.roles) - 1})",
            value = f"-# {list_roles(ctx, member)}",
            inline = False
        )

        e.set_author(
            icon_url = member.display_avatar.url,
            name = f"{member.global_name or member.display_name} ({member.name})",
            url = f"https://www.discord.com/users/{member.id}"
        )
        e.set_thumbnail(url = member.display_avatar.url)
        pos = await joinpos(ctx, member)
        p = f"{pos}" if pos > 0 else "**none**"
        e.set_footer(text = f"id: {member.id} ∙ join pos: {(p)}")

        await send(ctx, e)

    @commands.hybrid_command()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        e = embed(ctx, "", "")
        e.set_image(url = member.display_avatar.url)

        await send(ctx, e)

    @commands.hybrid_command()
    async def status(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        status, activity = fetch_status(ctx, member)

        await send(ctx, f"{status}\n{activity}")

    @commands.hybrid_command()
    async def boost(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        boosting = "boosting: **false**"

        if member.premium_since is not None:
            boosting = f"boosting: **true**, since: <t:{int(member.premium_since)}:D> (<t:{member.premium_since}:R>)"

        await send(ctx, f"-# {boosting}")

    @commands.hybrid_command()
    async def perms(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        perms = list_perms(member)
        pages = paginate(ctx, f"{member.global_name or member.display_name}'s perms - {len(perms)}", perms, formatter = lambda p: f"-# {p}")
        await send_pages(ctx, pages, buttons = ("prev", "next"))

async def setup(bot):
    await bot.add_cog(Member(bot))
