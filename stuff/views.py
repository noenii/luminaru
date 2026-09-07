import discord

class PageSearchModal(discord.ui.Modal, title = "Go to Page"):
    page_num = discord.ui.TextInput(
        label = "Page Number",
        placeholder = "Enter a Page Number",
        required = True,
        max_length = 5
    )

    def __init__(self, paginator_view):
        super().__init__()
        self.paginator_view = paginator_view

    async def on_submit(self, interaction: discord.Interaction):
        try:
            target_page = int(self.page_num.value) - 1
            max_pages = len(self.paginator_view.pages_data)

            if 0 <= target_page < max_pages:
                self.paginator_view.current_page = target_page
                self.paginator_view.update_view()
                await interaction.response.edit_message(
                    view = self.paginator_view
                )
            else:
                await interaction.response.send_message(
                    f"Invalid Page, Enter a Number Between 1 and {max_pages}",
                    ephemeral = True
                )
        except ValueError:
            await interaction.response.send_message("Enter a Number", ephemeral = True)

class Paginator(discord.ui.LayoutView):
    def __init__(
        self,
        containers: list[discord.ui.Container],
        author_id: int,
        buttons: list[str] = None
    ):
        super().__init__(timeout = 60)
        self.containers = containers
        self.author_id = author_id
        self.current_page = 0

        if buttons is None:
            buttons = ["prev", "next", "search", "exit"]

        self.buttons_map = {}
        if "prev" in buttons:
            btn = discord.ui.Button(emoji = "<:larrow:1546438657035075675>", style = discord.ButtonStyle.secondary)
            btn.callback = self.go_prev
            self.buttons_map["prev"] = btn

        if "next" in buttons:
            btn = discord.ui.Button(emoji = "<:rarrow:1546438717919469650>", style = discord.ButtonStyle.secondary)
            btn.callback = self.go_next
            self.buttons_map["next"] = btn

        if "search" in buttons:
            btn = discord.ui.Button(emoji = "<:search:1546438616190947369>", style = discord.ButtonStyle.secondary)
            btn.callback = self.go_search
            self.buttons_map["search"] = btn

        if "exit" in buttons:
            btn = discord.ui.Button(emoji = "<:stop:1546438775633092658>", style = discord.ButtonStyle.danger)
            btn.callback = self.go_exit
            self.buttons_map["exit"] = btn

        self.update_view()

    def update_view(self):
        self.clear_items()

        if "prev" in self.buttons_map:
            self.buttons_map["prev"].disabled = self.current_page == 0
        if "next" in self.buttons_map:
            self.buttons_map["next"].disabled = self.current_page == len(self.containers) - 1

        container = self.containers[self.current_page]

        action_row = discord.ui.ActionRow(*self.buttons_map.values())
        container.add_item(action_row)

        self.add_item(container)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("This Button is Not For You", ephemeral = True)
            return False
        return True

    async def go_prev(self, interaction: discord.Interaction):
        self.current_page -= 1
        self.update_view()
        await interaction.response.edit_message(view = self)

    async def go_next(self, interaction: discord.Interaction):
        self.current_page += 1
        self.update_view()
        await interaction.response.edit_message(view = self)

    async def go_search(self, interaction: discord.Interaction):
        await interaction.response.send_modal(PageSearchModal(self))

    async def go_exit(self, interaction: discord.Interaction):
        self.stop()
        await interaction.message.delete()

def chunk_list(items: list, per_page: int):
    for i in range(0, len(items), per_page):
        yield items[i : i + per_page]
