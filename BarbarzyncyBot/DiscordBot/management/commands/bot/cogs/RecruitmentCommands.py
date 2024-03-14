import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure

import os
from io import StringIO
import emoji





class RecruitmentCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.officer_role_id = int(self.bot.settings["OFFICER_ROLE_ID"])
        self.recruitment_channel_id = int(self.bot.settings["RECRUITMENT_CHANNEL_ID"])
        self.recruitment_category_id = int(self.bot.settings["RECRUITMENT_CATEGORY_ID"])
        self.accepted_channel_id = int(self.bot.settings["ACCEPTED_CHANNEL_ID"])
        self.declined_channel_id = int(self.bot.settings["DECLINED_CHANNEL_ID"])
        self.no_response_channel_id = int(self.bot.settings["NO_RESPONSE_CHANNEL_ID"])

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send(
                "Niestety, nie masz uprawnień do wykonania tej komendy tutaj.",
                ephemeral=True,
            )
            return True
        return False

    async def check_officer_role(self, ctx):
        officer_role = ctx.guild.get_role(self.officer_role_id)
        if officer_role is None:
            self.bot.logger.error(f"Nie znaleziono roli {self.officer_role_id}")
            return False

        user_roles = ctx.author.roles
        return any(
            role.id == self.officer_role_id or role.position > officer_role.position
            for role in user_roles
        )

    async def check_channel(self, ctx):
        if (
            ctx.channel.category_id == self.recruitment_category_id
            and ctx.channel.id != self.recruitment_channel_id
        ):
            return True
        else:
            return False

    async def close_recruitment(self, ctx, result_channel_id):
        await ctx.reply(f"Przenoszę podanie do archiwum", ephemeral=True)
        summary = {"Oficer": f"{ctx.author.mention}"}
        messages = []
        async for message in ctx.channel.history(oldest_first=True):
            if message.embeds:
                for embed in message.embeds:
                    for field in embed.fields:
                        messages.append(emoji.demojize(f"{field.name}:"))
                        messages.append(emoji.demojize(f"{field.value}"))
                        messages.append("")
                recruitment_embed = message.embeds[0]
                summary["Typ podania"] = recruitment_embed.title
                summary["Użytkownik"] = recruitment_embed.author.name
                messages.append("==============================")
            else:
                messages.append(emoji.demojize(f"{message.author.display_name}:"))
                messages.append(f"  {message.clean_content}")
                messages.append("")
        summary_embed = discord.Embed(title="Podsumowanie rekrutacji")

        for label, value in summary.items():
            summary_embed.add_field(name=label, value=value)
        file = StringIO(os.linesep.join(messages))
        discord_file = discord.File(
            fp=file,
            filename="historia_wiadomosci.txt",
            spoiler=False,
        )
        result_channel = ctx.guild.get_channel(result_channel_id)
        await result_channel.send(file=discord_file, embed=summary_embed)
        if ctx.channel is not None:
            await ctx.channel.delete()

    @commands.hybrid_command(description="Zatwierdzenie podania")
    @commands.check(lambda ctx: ctx.cog.check_officer_role(ctx))
    @commands.check(lambda ctx: ctx.cog.check_channel(ctx))
    async def accept(self, ctx):
        await self.close_recruitment(ctx, self.accepted_channel_id)

    @commands.hybrid_command(description="Odrzucenie podania")
    @commands.check(lambda ctx: ctx.cog.check_officer_role(ctx))
    @commands.check(lambda ctx: ctx.cog.check_channel(ctx))
    async def decline(self, ctx):
        await self.close_recruitment(ctx, self.declined_channel_id)

    @commands.hybrid_command(description="Anulowanie podania z powody braku kontaktu")
    @commands.check(lambda ctx: ctx.cog.check_officer_role(ctx))
    @commands.check(lambda ctx: ctx.cog.check_channel(ctx))
    async def no_response(self, ctx):
        await self.close_recruitment(ctx, self.no_response_channel_id)


async def setup(bot):
    await bot.add_cog(RecruitmentCommands(bot))
