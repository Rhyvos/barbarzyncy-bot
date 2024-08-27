import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.logger.info(f"{self.__class__.__name__} Cog has been loaded\n-----")


    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.defer(ephemeral=True)
            await ctx.send(
                "Niestety, nie masz uprawnień do wykonania tej komendy tutaj.",
                ephemeral=True,
            )
            return True
        return False

    @commands.hybrid_command(description="Stops the bot")
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.defer(ephemeral=True)
        await ctx.send(f'Stopping Bot!')
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Stop(bot))