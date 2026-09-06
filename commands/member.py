import discord

from discord.ext import commands

from stuff.funcs import container, fetch_status, joinpos, list_roles, list_perms, ts
from stuff.views import paginate, send_pages

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def member(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        e = discord.Embed()

        e.add_field(
            name = "Joined",
            value = f"> {ts(int(member.joined_at.timestamp()), 'D')} ({ts(int(member.joined_at.timestamp()), 'R')})",
            inline = False
        )

        e.add_field(
            name = "Created",
            value = f"> {ts(int(member.created_at.timestamp()), 'D')} ({ts(int(member.created_at.timestamp()), 'R')})",
            inline = False
        )

        rc = len(member.roles) - 1
        msg = f"-# {list_roles(ctx, member)}" if rc > 0 else "None"

        e.add_field(
            name = f"Roles ({len(member.roles) - 1})",
            value = msg,
            inline = False
        )

        e.set_author(
            icon_url = member.display_avatar.url,
            name = f"{member.global_name or member.display_name} ({member.name})",
            url = f"https://www.discord.com/users/{member.id}"
        )

        e.set_thumbnail(url = member.display_avatar.url)
        pos = await joinpos(ctx, member)
        p = f"{pos}" if pos > 0 else "**None**"
        e.set_footer(text = f"ID: {member.id} ∙ Join Pos: {(p)}")

        await ctx.send(embed = e)

    @commands.hybrid_command()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        v = container(
            ctx,
            image = member.display_avatar.url,
            buttons = [(member.display_avatar.url, None, "<:discord:1546171146893004870>")]
        )

        await ctx.send(view = v)

    @commands.hybrid_command()
    async def status(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        status, activity = fetch_status(ctx, member)

        await ctx.send(f"{status}\n{activity}")

    @commands.hybrid_command()
    async def boost(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author

        if member.premium_since:
            await ctx.send(f"-# Boosting: **True**, Since: {ts(int(member.premium_since.timestamp()), 'D')} ({ts(int(member.premium_since.timestamp()), 'R')})")
        else:
            await ctx.send("-# Boosting: **False**")

    @commands.hybrid_command()
    async def perms(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        perms = list_perms(member)
        pages = paginate(
            ctx,
            t = f"{member.global_name or member.display_name}'s Perms - {len(perms)}",
            items = perms,
            formatter = lambda p: f"-# {p}"
        )
        if len(pages) == 1:
            await ctx.send(embed = pages[0])
        else:
            await send_pages(ctx, pages, buttons = ("prev", "next"))

async def setup(bot):
    await bot.add_cog(Member(bot))
