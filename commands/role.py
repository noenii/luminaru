import discord

from discord.ext import commands

from stuff.funcs import embed, send, ts, perm_check

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def role(self, ctx: commands.Context, role: discord.Role = None):
        if not role:
            raise commands.BadArgument

        e = embed(
            ctx,
            f"**{role.name}**",
            f"-# There are **{len(role.members)}** members with this role\n"
            f"-# This role **{"is" if role.hoist else "isn't"}** hoisted"
        )

        e.add_field(
            name = "__**Information**__ ",
            value = f"-# Created: {ts(int(role.created_at.timestamp()), 'D')} ({ts(int(role.created_at.timestamp()), 'R')})\n"
            f"-# Dangerous: **{perm_check(role)}**",
            inline = False
        )

        await send(ctx, e)

    @commands.hybrid_command()
    async def roleinfo(self, ctx: commands.Context, role: discord.Role = None):
        if not role:
            raise commands.BadArgument

        e = embed(
            ctx,
            "",
            f"Hex: **{role.color.value}**\n"
            f"ID: **{role.id}**\n"
            f"Pos: **{role.position}**\n"
            f"Hoist: **{role.hoist}**\n"
            f"Mention: **{role.mentionable}**"
        )

        await send(ctx, e)

# need: withrole, roles

async def setup(bot):
    await bot.add_cog(Role(bot))
