import discord

from math import ceil

from stuff.funcs import embed

class PageModal(discord.ui.Modal, title = "Go to Page"):
    page = discord.ui.TextInput(
        label = "Page Number",
        placeholder = "Enter a page number..."
    )

    def __init__(self, view):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            page = int(self.page.value)
        except ValueError:
            return await interaction.response.send_message(
                "Invalid Page",
                ephemeral = True
            )

        if not 1 <= page <= len(self.view.pages):
            return await interaction.response.send_message(
                f"enter a number between 1 and {len(self.view.pages)}.",
                ephemeral = True
            )

        self.view.index = page - 1
        self.view.update_buttons()

        await interaction.response.edit_message(
            embed = self.view.pages[self.view.index],
            view = self.view
        )


class Paginator(discord.ui.View):
    def __init__(self, pages, author, *, timeout = 120, buttons = ("first", "prev", "page", "next", "last")):
        super().__init__(timeout=timeout)

        self.pages = pages
        self.author = author
        self.index = 0
        self.buttons = set(buttons)

        if "first" not in self.buttons:
            self.remove_item(self.first)

        if "prev" not in self.buttons:
            self.remove_item(self.prev)

        if "page" not in self.buttons:
            self.remove_item(self.page)

        if "next" not in self.buttons:
            self.remove_item(self.next)

        if "last" not in self.buttons:
            self.remove_item(self.last)

        self.update_buttons()

    async def interaction_check(self, interaction):
        if interaction.user != self.author:
            await interaction.response.send_message(
                "you cant use this",
                ephemeral = True
            )
            return False
        return True

    def update_buttons(self):
        last = len(self.pages) - 1

        if "first" in self.buttons:
            self.first.disabled = self.index == 0

        if "prev" in self.buttons:
            self.prev.disabled = self.index == 0

        if "next" in self.buttons:
            self.next.disabled = self.index == last

        if "last" in self.buttons:
            self.last.disabled = self.index == last

        if "page" in self.buttons:
            self.page.label = f"{self.index + 1}/{len(self.pages)}"

    async def update(self, interaction):
        self.update_buttons()

        await interaction.response.edit_message(
            embed=self.pages[self.index],
            view=self
        )

    @discord.ui.button(emoji = "<<", style=discord.ButtonStyle.primary)
    async def first(self, interaction, button):
        self.index = 0
        await self.update(interaction)

    @discord.ui.button(label = "<", style=discord.ButtonStyle.primary)
    async def prev(self, interaction, button):
        self.index -= 1
        await self.update(interaction)

    @discord.ui.button(label = "1/1", style=discord.ButtonStyle.secondary)
    async def page(self, interaction, button):
        await interaction.response.send_modal(PageModal(self))

    @discord.ui.button(label = ">", style=discord.ButtonStyle.primary)
    async def next(self, interaction, button):
        self.index += 1
        await self.update(interaction)

    @discord.ui.button(label = ">>", style=discord.ButtonStyle.primary)
    async def last(self, interaction, button):
        self.index = len(self.pages) - 1
        await self.update(interaction)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True

        if hasattr(self, "message"):
            await self.message.edit(view=self)

async def send_pages(ctx, pages, *, timeout = 120, buttons = ("first", "prev", "page", "next", "last")):
    view = Paginator(
        pages = pages,
        author = ctx.author,
        timeout = timeout,
        buttons = buttons
    )

    msg = await ctx.send(
        embed = pages[0],
        view = view
    )

    view.message = msg

def paginate(ctx, title: str, items: list, a = False, f = False, *, per_page: int = 10, formatter = str):
    if not items:
        items = ["None"]

    total = ceil(len(items) / per_page)

    pages = []

    for page, start in enumerate(range(0, len(items), per_page), start = 1):
        chunk = items[start:start + per_page]

        e = embed(
            ctx,
            title,
            "\n".join(formatter(item) for item in chunk)
        )

        if a:
            e.set_author
        if f:
            e.set_footer(text = f"{page}/{total}")

        pages.append(e)

    return pages
