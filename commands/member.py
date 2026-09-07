import discord

from discord.ext import commands

from stuff.funcs import container, fetch_status, joinpos, list_roles, list_perms, ts
from stuff.views import Paginator, chunk_list
from setup.config import EMBED_COLOR

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
        if member.guild_permissions.administrator:
            return await ctx.send("-# User has Administrator")

        p = [
            f"**{perm.replace('_', ' ').title()}**"
            for perm, value in member.guild_permissions
            if value
        ]

        if not p:
            return await ctx.send("-# User Has no Perms")

        chunks = list(chunk_list(p, 10))
        total_pages = len(chunks)

        containers = []
        for i, chunk in enumerate(chunks, start=1):
            c = discord.ui.Container()

            c.add_item(discord.ui.Section(
                discord.ui.TextDisplay(f"## {member.display_name}'s permissions — {len(p)}"), # idk why these dashes look better than regular dashes
                accessory = discord.ui.Thumbnail(member.display_avatar.url)
            ))
            c.add_item(discord.ui.Separator())

            c.add_item(discord.ui.TextDisplay("\n".join(chunk)))
            c.add_item(discord.ui.Separator())

            c.add_item(discord.ui.TextDisplay(f"-# Page {i}/{total_pages}"))

            containers.append(c)

        view = Paginator(
            containers = containers,
            author_id = ctx.author.id,
            buttons = ["prev", "next", "search", "exit"]
        )
        await ctx.send(view = view)

async def setup(bot):
    await bot.add_cog(Member(bot))
