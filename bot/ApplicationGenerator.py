import discord
from discord import ui
from asgiref.sync import sync_to_async
from functools import partial

from DynamicView import DynamicView
from EditModal import EditModal
from utils.bot_logger import bot_logger

from BotQuestions.models import Question


class ApplicationGenerator:
    logger = bot_logger("ApplicationGenerator")

    def __init__(self, bot, req_type, user):
        self.bot = bot
        self.req_type = req_type
        self.user = user
        self.channel_name = f"{self.req_type.type_name}-{self.user.name}".lower()
        self.logger.info(
            f"New recruitment application User:{self.user.name} Type:{self.req_type.type_name}"
        )

    async def check_existing_channel(self):
        category_id = int(self.bot.settings["RECRUITMENT_CATEGORY_ID"])
        category = self.bot.get_channel(category_id)

        if not category:
            self.logger.info(f"Category with ID {category_id} not found")
            return False

        existing_channels = [
            ch for ch in category.channels if self.user.name in ch.name
        ]
        return bool(existing_channels)

    async def generate_application_questions(self):
        questions = await sync_to_async(list)(
            Question.objects.filter(requirement_type=self.req_type, enabled=True)
        )
        category_id = int(self.bot.settings["RECRUITMENT_CATEGORY_ID"])
        category = self.bot.get_channel(category_id)

        if not category:
            self.logger.info(f"Category with ID {category_id} not found")
            return False

        try:
            channel = await category.create_text_channel(self.channel_name)
        except Exception:
            self.logger.warning(
                f"Failed to create channel {self.channel_name} in category ID {category_id}"
            )
            return False

        embed = discord.Embed(
            title=f"Recruitment {self.req_type.type_name}",
            color=discord.Color.blue(),
        )
        embed.set_author(name=self.user.name, icon_url=self.user.avatar.url)
        for question in questions:
            embed.add_field(
                name=f"{question.question_text}", value="<not filled in>", inline=False
            )

        view = DynamicView(self.channel_name, self.logger)
        self._add_buttons_to_view(view)
        self.bot.add_view(view)
        channel_permissions = channel.overwrites_for(self.user)
        channel_permissions.update(
            view_channel=True,
            send_messages=True,
            read_messages=True,
            read_message_history=True,
        )
        await channel.set_permissions(self.user, overwrite=channel_permissions)

        await channel.send(
            f"Witaj {self.user.mention}! Rozpoczynam proces rekrutacyjny na {self.req_type.type_name}."
        )
        await channel.send(embed=embed, view=view)

        return True

    async def on_button_click_remove_channel(self, interaction, button):
        channel = interaction.channel
        application_owner = channel.name.split("-")[-1]

        if interaction.user.name == application_owner:
            await channel.delete()
            self.bot.remove_user_views(application_owner)
        else:
            await interaction.response.send_message(
                f"Podanie możne usunąć wyłącznie {application_owner}",
                ephemeral=True,
            )

    async def on_button_click_edit_application(self, interaction, button):
        channel = interaction.channel
        application_owner = channel.name.split("-")[-1]
        if interaction.user.name != application_owner:
            await interaction.response.send_message(
                f"Podanie możne edytować wyłącznie {application_owner}",
                ephemeral=True,
                delete_after=10,
            )
            return

        await interaction.response.send_message(
            "Przetwarzam żądanie...", ephemeral=True, delete_after=5
        )
        await self._process_edit_application_interaction(interaction)

    async def _process_edit_application_interaction(self, interaction):
        channel = interaction.channel
        views = await self._generate_application_buttons(channel)

        for view, field in views:
            await interaction.followup.send(
                f"**{field.name}**", view=view, ephemeral=True
            )

        if len(views) == 0:
            await interaction.followup.send(
                "Nie znaleziono pytań w podaniu.", ephemeral=True
            )

    async def on_button_click_edit_application_field(
        self, interaction, button, message, field_index
    ):
        channel = self.bot.get_channel(message.channel.id)
        if channel is None:
            self.logger.warning("Nie można znaleźć kanału.")
            return
        try:
            message_refreshed = await channel.fetch_message(message.id)
        except discord.NotFound:
            self.logger.warning("Nie można znaleźć wiadomości.")
            return
        except discord.Forbidden:
            self.logger.warning("Brak uprawnień do pobrania wiadomości.")
            return
        modal = EditModal(
            title=f"{message.embeds[0].fields[field_index].name[:42]}...",
            channel_id=message.channel.id,
            message=message_refreshed,
            field_index=field_index,
            bot=self.bot,
        )
        await interaction.response.send_modal(modal)

    async def regenerate_application(self):
        view = DynamicView(self.channel_name, self.logger)
        self._add_buttons_to_view(view)
        self.bot.add_view(view)
        channel = discord.utils.get(
            self.bot.get_all_channels(), name=self.channel_name.lower()
        )
        if channel is not None:
            await self._generate_application_buttons(channel)
        else:
            self.logger.info(
                f"Kanał {self.channel_name.lower()} nie został znaleziony."
            )

    async def _generate_application_buttons(self, channel):
        embeded_message = False
        views = []
        async for message in channel.history(limit=200):
            if embeded_message:
                break

            for embed in message.embeds:
                embeded_message = True
                for index, field in enumerate(embed.fields, start=0):
                    view = self._generate_fill_in_button(index, message)
                    views.append((view, field))
        return views
    

    def _generate_fill_in_button(self, index, message):
        view = DynamicView(self.channel_name, self.logger, timeout=7200)
        view.add_button(
            f"field:{index}",
            "Uzupełnij",
            partial(
                self.on_button_click_edit_application_field,
                message=message,
                field_index=index,
            ),
            style=discord.ButtonStyle.blurple,
        )
        return view

    def _add_buttons_to_view(self, view):
        view.add_button(
            "edit_application",
            "Edytuj podanie",
            self.on_button_click_edit_application,
            style=discord.ButtonStyle.green,
        )
        view.add_button(
            "remove_channel",
            "Usuń podanie",
            self.on_button_click_remove_channel,
            style=discord.ButtonStyle.red,
        )
