import discord

from discord.ext import commands

from stuff.funcs import ts
# from stuff.views import paginate, send_pages

class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def channel(self, ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        channel = channel or ctx.channel

        topic = getattr(channel, 'topic', None) or ""
        e = discord.Embed(
            title = f"#{channel.name} — ({channel.id})",    # all em dashes were inserted by a real person btw
            description = f"\n{topic}" if topic else ""
        )
        e.url = f"https://discord.com/channels/{ctx.guild.id}/{channel.id}"
        e.set_author(name = f"{ctx.guild.name}", icon_url = ctx.guild.icon.url if ctx.guild.icon else None)

        e.add_field(
            name = "Created",
            value = f"{ts(int(channel.created_at.timestamp()), 'D')} ({ts(int(channel.created_at.timestamp()), 'R')})",
            inline = False
        )

        match channel:
            case discord.TextChannel():
                e.add_field(
                    name = "Details",
                    value = f"> NSFW: **{channel.is_nsfw()}**\n"
                    f"> Category: **{channel.category.name if channel.category else "None"}**\n"
                    f"> Slowmode: {f"**{channel.slowmode_delay} s**" if channel.slowmode_delay else "**None**"}",
                    inline = True
                )

            case discord.VoiceChannel() | discord.StageChannel():
                e.add_field(
                    name = "Details",
                    value = f"> Type: **{"Stage" if isinstance(channel, discord.StageChannel) else "Voice"}**\n"
                    f"> Bitrate: **{channel.bitrate // 1000} kbps**\n"
                    f"> User Limit: **{channel.user_limit if channel.user_limit else 'Unlimited'}**\n"
                    f"> Category: **{channel.category.name if channel.category else "None"}**",
                    inline = True
                )

            case discord.Thread():
                e.add_field(
                    name = "Details",
                    value = f"> Type: **Thread**\n"
                    f"> Parent Channel: {channel.parent.mention if channel.parent else 'Unknown'}\n"
                    f"> Archived: **{"True" if channel.archived else "False"}**\n"
                    f"> Locked: **{"True" if channel.locked else "False"}**\n"
                    f"> Slowmode: {f'**{channel.slowmode_delay}s**' if channel.slowmode_delay else '**None**'}",
                    inline = True
                )
                e.add_field(
                    name = "Thread Stats",
                    value = f"> Owner: <@{channel.owner_id}>\n"
                    f"> Members: **{channel.member_count}**",
                    inline = True
                )

            case discord.ForumChannel():
                e.add_field(
                    name = "Details",
                    value = f"> Type: **Forum**\n"
                    f"> Category: **{channel.category.name if channel.category else "None"}**\n"
                    f"> Delay: **{f'{channel.default_auto_archive_duration} m' if channel.default_auto_archive_duration else 'None'}**\n"
                    f"> Total Tags: **{len(channel.available_tags)}**",
                    inline = True
                )

            case discord.CategoryChannel():
                e.add_field(
                    name = "Details",
                    value = f"> Type: **Category**\n"
                    f"> Text Channels: **{len(channel.text_channels)}**\n"
                    f"> Voice Channels: **{len(channel.voice_channels)}**\n"
                    f"> Total Channels: **{len(channel.channels)}**",
                    inline = True
                )

        if hasattr(channel, "invites"):
            try:
                i = await channel.invites()
                if i:
                    invite_lines = [f"[{inv.code}](https://discord.gg/{inv.code}) — **{inv.uses}** uses" for inv in i[:3]]
                    iv = "\n".join(invite_lines)
                else:
                    iv = "No active invites"
            except discord.Forbidden:
                iv = "Missing Permissions"

            e.add_field(name = "Invites", value = iv, inline = True)

        await ctx.send(embed = e)
'''
    @commands.hybrid_command()
    async def channelperms(self, ctx: commands.Context, channel: discord.abc.GuildChannel = None):
        channel = channel or ctx.channel

        if not channel.overwrites:
            return await ctx.send(f"-# {channel.mention} has no Permission Overrides.")

        entries = []
        for target, overwrite in channel.overwrites.items():
            if isinstance(target, discord.Role):
                target_str = f"-# Role: {target.mention}"
            elif isinstance(target, discord.Member):
                target_str = f"-# Member: {target.mention}"
            else:
                target_str = f"-# Target: {target.id}"

            allowed_perms = [perm.replace("_", " ").title() for perm, val in overwrite if val is True]
            denied_perms = [perm.replace("_", " ").title() for perm, val in overwrite if val is False]

            allows_text = "**, **".join(allowed_perms) if allowed_perms else "None"
            denies_text = "**, **".join(denied_perms) if denied_perms else "None"

            entry = (
                f"{target_str}\n"
                f"> Allowed: **{allows_text}**\n"
                f"> Denied: **{denies_text}**"
            )

            entries.append(entry)

        pages = paginate(
            ctx,
            t = f"Permissions for #{channel.name}",
            items = entries,
            per_page = 2,
            formatter = lambda item: f"{item}\n"
        )

        if len(pages) == 1:
            await ctx.send(embed = pages[0])
        else:
            await send_pages(ctx, pages, buttons = ("prev", "page", "next"))

    @commands.hybrid_command()
    async def threads(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        act = channel.threads if hasattr(channel, "threads") else []

        try:
            art = []
            async for thread in channel.archived_threads(limit = 50):
                art.append(thread)
        except (discord.Forbidden, AttributeError):
            art = []

        a = act + art

        if not a:
            return await ctx.send(f"-# No threads found in {channel.mention}")

        entries = []

        for thread in a:
            entries.append(
                f"{thread.mention} (**{thread.id}**)\n"
                f"> Status: **{"Locked" if thread.locked else ("Archived" if thread.archived else "Active")}**\n"
                f"> Parent: {thread.parent.mention if thread.parent else "**Unknown**"}\n"
                f"> Members: {thread.member_count}\n"
                f"> Owner: <@{thread.owner_id}>"
            )

        pages = paginate(
            ctx,
            t = f"Threads in #{channel.name}",
            items = entries,
            per_page = 5,
            formatter = lambda item: f"{item}\n"
        )

        if len(pages) == 1:
            await ctx.send(embed = pages[0])
        else:
            await send_pages(ctx, pages, buttons = ("prev", "next"))
'''
async def setup(bot):
    await bot.add_cog(Channel(bot))
