import discord
from discord.ext import commands

from django.conf import settings as project_settings

from dotenv import dotenv_values
from asgiref.sync import sync_to_async

from BotQuestions.models import RequirementType
from WelcomeMessage.models import WelcomeMessage
from .DynamicView import DynamicView
from .ApplicationGenerator import ApplicationGenerator
from .utils.bot_logger import bot_logger


class BotBarbarzynca(commands.Bot):
    """
    Custom Discord bot class for handling recruitment and onboarding processes.
    """

    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        intents.members = True

        super().__init__(command_prefix=command_prefix, intents=intents)

        # List of bot extensions to load.
        self.initial_extensions = [
            "DiscordBot.management.commands.bot.cogs.RecruitmentCommands"
        ]

        # Load settings from .env file using project settings.
        self.settings = dotenv_values(project_settings.ENV_PATH)
        self.logger = bot_logger("BotBarbarzynca")

    async def setup_hook(self):
        """Loads all initial extensions for the bot."""
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_button_click(self, interaction, button):
        """Handles button click events."""
        if button.custom_id.startswith("requirement_type"):
            # Extract the requirement type ID from the button custom ID.
            req_type_id = int(button.custom_id.split(":")[-1])
            req_type = await sync_to_async(RequirementType.objects.get)(id=req_type_id)

            user = interaction.user
            application_generator = ApplicationGenerator(self, req_type, user)

            if await application_generator.check_existing_channel():
                self.logger.info(f"User {user.name} already has an active application.")
                await interaction.response.send_message(
                    "You already have an active application. Please finish it before starting a new one.",
                    ephemeral=True,
                    delete_after=10,
                )
                return

            if await application_generator.generate_application_questions():
                await interaction.response.defer()
            else:
                await interaction.response.send_message(
                    "Something went wrong. Please report this to the officers.",
                    ephemeral=True,
                    delete_after=10,
                )

    async def on_ready(self):
        """Executed when the bot is ready."""
        self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.tree.sync()

        recruitment_channel = self.get_channel(
            int(self.settings["RECRUITMENT_CHANNEL_ID"])
        )
        if recruitment_channel:
            requirement_types = await sync_to_async(list)(
                RequirementType.objects.filter(enabled=True)
            )
            # Clear previous messages sent by the bot in the recruitment channel.
            async for message in recruitment_channel.history(limit=200):
                if message.author == self.user:
                    await message.delete()

            view = DynamicView("requirement_type")
            for req_type in requirement_types:
                button_label = f"Apply for {req_type.type_name}"
                view.add_button(req_type.id, button_label, self.on_button_click)

            welcome_message_obj = await sync_to_async(list)(
                WelcomeMessage.objects.all()
            )
            welcome_message = (
                welcome_message_obj[0].message
                if welcome_message_obj
                else "Select the type of application:"
            )

            await recruitment_channel.send(welcome_message, view=view)

        else:
            self.logger.info(
                f"Recruitment channel with ID {self.settings['RECRUITMENT_CHANNEL_ID']} not found."
            )

        await self._regenerate_all_applications()

    async def _regenerate_all_applications(self):
        """Regenerates all applications for the recruitment category."""
        category_id = int(self.settings["RECRUITMENT_CATEGORY_ID"])
        category = self.get_channel(category_id)
        self.logger.info(f"Regenerating all applications in category: {category.name} (ID: {category.id})")
        if category:
            for channel in category.channels:
                if channel.id != int(self.settings["RECRUITMENT_CHANNEL_ID"]):
                    req_type_name, username = channel.name.split("-")
                    req_types = await sync_to_async(list)(
                        RequirementType.objects.filter(
                            type_name__icontains=req_type_name
                        )
                    )

                    user = discord.utils.get(self.users, name=username)
                    for req_type in req_types:
                        application_generator = ApplicationGenerator(
                            self, req_type, user
                        )
                        await application_generator.regenerate_application()


    async def on_resumed(self):
        self.logger.info(f"Resumed session as {self.user} (ID: {self.user.id})")
        await self.tree.sync()

        recruitment_channel = self.get_channel(
            int(self.settings["RECRUITMENT_CHANNEL_ID"])
        )
        if recruitment_channel:
            self.logger.info(f"Recruitment channel found {recruitment_channel.name} (ID: {recruitment_channel.id})")
            requirement_types = await sync_to_async(list)(
                RequirementType.objects.filter(enabled=True)
            )
            # Clear previous messages sent by the bot in the recruitment channel.
            async for message in recruitment_channel.history(limit=200):
                if message.author == self.user:
                    await message.delete()

            view = DynamicView("requirement_type")
            for req_type in requirement_types:
                button_label = f"Apply for {req_type.type_name}"
                view.add_button(req_type.id, button_label, self.on_button_click)

            welcome_message_obj = await sync_to_async(list)(
                WelcomeMessage.objects.all()
            )
            welcome_message = (
                welcome_message_obj[0].message
                if welcome_message_obj
                else "Select the type of application:"
            )

            await recruitment_channel.send(welcome_message, view=view)

        else:
            self.logger.info(
                f"Recruitment channel with ID {self.settings['RECRUITMENT_CHANNEL_ID']} not found."
            )

        await self._regenerate_all_applications()

    def get_recruitment_category(self):
        """Returns the recruitment category channel."""
        return self.get_channel(int(self.settings["RECRUITMENT_CATEGORY_ID"]))
