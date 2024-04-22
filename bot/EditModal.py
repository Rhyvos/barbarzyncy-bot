import discord
from discord import ui

from utils.bot_logger import bot_logger


class EditModal(ui.Modal):
    """Modal for editing message embeds."""

    logger = bot_logger("EditModal")

    def __init__(self, title, channel_id, message, field_index, bot):
        """Initialize the modal for editing a message."""
        super().__init__(title=title)
        self.message_id = message.id
        self.field_index = field_index
        self.channel_id = channel_id
        self.bot = bot

        self.add_item(
            ui.TextInput(
                label="Edit:",
                style=discord.TextStyle.paragraph,
                default=message.embeds[0].fields[field_index].value,
                placeholder="<not provided>",
                max_length=1024,
            )
        )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle the user submitting the modal."""
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            self.logger.warning("Channel not found.")
            return

        try:
            message = await channel.fetch_message(self.message_id)
        except discord.NotFound:
            self.logger.warning("Message not found.")
            return
        except discord.Forbidden:
            self.logger.warning("Missing permissions to fetch the message.")
            return

        original_embed = message.embeds[0]
        new_embed = discord.Embed(
            title=original_embed.title, description=original_embed.description
        )

        for index, field in enumerate(original_embed.fields):
            if index == self.field_index:
                new_embed.add_field(
                    name=field.name, value=self.children[0].value, inline=field.inline
                )
            else:
                new_embed.add_field(
                    name=field.name, value=field.value, inline=field.inline
                )

        new_embed.set_author(
            name=original_embed.author.name, icon_url=original_embed.author.icon_url
        )

        await message.edit(embed=new_embed)
        await interaction.response.defer()