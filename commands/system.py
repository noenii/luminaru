import discord, time

from discord.ext import commands
from stuff.services import system_stats
from stuff.funcs import embed, send, format_bytes, fmt_time, ts
from setup.config import SUCCESS, LOADING

class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name = "ping",
        description = "View Ping",
        help = "View Ping Stats"
    )
    async def ping(self, ctx: commands.Context):
        s = system_stats(self.bot, self.bot.start_time)

        start = time.time()
        message = await ctx.reply(f"Pinging...", mention_author=False)
        end = time.time()

        if ctx.message:
            try:
                await ctx.message.add_reaction(LOADING)
            except:
                pass

        l = round((end - start) * 1000)

        e = embed(
            ctx,
            "Network Stats",
            f"> API: `{s['ping']} ms`\n"
            f"> Latency: `{l} ms`\n"
            f"> Status: `{'Good' if s['ping'] < 300 else 'OK' if s['ping'] < 600 else 'Bad'}`\n"
            f"> Sent: `{format_bytes(s['sent'])}`\n"
            f"> Received: `{format_bytes(s['recv'])}`",
            True
        )

        if ctx.message:
            try:
                emoji = discord.PartialEmoji.from_str(LOADING)
                await ctx.message.remove_reaction(emoji, self.bot.user)
                await ctx.message.add_reaction(SUCCESS)
            except:
                pass

        await message.edit(content = None, embed = e)

    @commands.hybrid_command(
        name = "system",
        description = "View System Stats",
        help = "View System Stats"
    )
    async def system(self, ctx: commands.Context):
        s = system_stats(self.bot, self.bot.start_time)
        await send(
            ctx,
            "System Stats",
            f"> CPU: `{s['cpu']}%`\n"
            f"> Cores: `{s['cores']}`\n"
            f"> Threads: `{s['threads']}`\n"
            f"> RAM: `{format_bytes(s['ram'])}`\n"
            f"> RAM%: `{s['ram_pct']}%`\n"
            f"> DISK%: `{s['disk_pct']}%`",
        )

    @commands.hybrid_command(
        name = "env",
        description = "View Bot Enviroment",
        help = "Displays System Info when Requested"
    )
    async def env(self, ctx: commands.Context):
        s = system_stats(self.bot, self.bot.start_time)
        await send(
            ctx,
            "Enviroment Info",
            f"> Python: `{s['py']}`\n"
            f"> Discord: `{s['dpy']}`\n"
            f"> OS: `{s['os']} {s['vers']}`\n"
            f"> Arch: `{s['arch']}`\n"
            "> Dir: `/bot`"
        )

    @commands.hybrid_command(
        name = "uptime",
        description = "View Uptime",
        help = "View Uptime Stats"
    )
    async def uptime(self, ctx: commands.Context):
        s = system_stats(self.bot, self.bot.start_time)
        await send(
            ctx,
            "Uptime Info",
            f"> Uptime: {ts(self.bot.start_time, "R")}\n"
            f"> Bot Start: {ts(self.bot.start_time, "F")}\n"
            f"> Sys Start: {ts(s['sys_start'], "F")}"
        )

async def setup(bot):
    await bot.add_cog(system(bot))
