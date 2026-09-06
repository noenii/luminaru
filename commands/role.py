import discord

from discord.ext import commands

from stuff.funcs import ts, perm_check, list_roles
from stuff.views import paginate, send_pages

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def role(self, ctx: commands.Context, role: discord.Role):
        e = discord.Embed(
            title = f"**{role.name}**",
            description = f"-# There are **{len(role.members)}** members with this role\n"
            f"-# This role **{'is' if role.hoist else 'isn\'t'}** hoisted"
        )

        e.add_field(
            name = "__**Information**__ ",
            value = f"-# Created: {ts(int(role.created_at.timestamp()), 'D')} ({ts(int(role.created_at.timestamp()), 'R')})\n"
            f"-# Dangerous: **{perm_check(role)}**",
            inline = False
        )

        await ctx.send(embed = e)

    @commands.hybrid_command()
    async def roleinfo(self, ctx: commands.Context, role: discord.Role):
        await ctx.send(f"-# Role: **{role.name}**, ID: **{role.id}**, Pos: **{role.position}**, Hoist: **{role.hoist}**, Mention: **{role.mentionable}**")

    @commands.hybrid_command()
    async def roles(self, ctx: commands.Context, member: discord.Member = None):
        if member:
            if len(member.roles) == 1:
                return await ctx.send("-# Member has no Roles")

            e = discord.Embed(
                title = f"**{member.name}**'s Roles",
                description = f"-# {list_roles(ctx, member)}"
            )

            return await ctx.send(embed = e)

        r = [i for i in reversed(ctx.guild.roles) if not i.is_default()]

        if not r:
            return await ctx.send("-# This Server has no Roles")

        pages = paginate(
            ctx = ctx,
            t = f"**Roles in {ctx.guild.name}** (**{len(r)}**)",
            items = r,
            per_page = 20,
            formatter = lambda i: f"{i.mention} - {len(i.members)}"
        )

        await send_pages(ctx, pages, buttons = ("prev", "next"))

    @commands.hybrid_command()
    async def withrole(self, ctx: commands.Context, role: discord.Role):
        if not role.members:
            return await ctx.send("-# Role has no Members")

        pages = paginate(
            ctx = ctx,
            t = f"**{role.name}** - **{len(role.members)}**",
            items = role.members,
            per_page = 15,
            formatter = lambda m: f"{m.mention}"
        )

        if len(pages) == 1:
            await ctx.send(embed = pages[0])
        else:
            await send_pages(ctx, pages, buttons = ("prev", "next"))

async def setup(bot):
    await bot.add_cog(Role(bot))
