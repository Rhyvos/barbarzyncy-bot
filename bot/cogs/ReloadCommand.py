import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure

class ReloadCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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

    @commands.hybrid_command(description="Reloads a cog")
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reloads a cog"""
        await ctx.defer(ephemeral=True)
        try:
            extension = f'cogs.{cog}'
            if extension in self.bot.extensions:
                self.bot.logger.info(f"Unloading {cog}...")
                await self.bot.unload_extension(extension)

            self.bot.logger.info(f"Loading {cog}...")
            await self.bot.load_extension(extension)
            await ctx.send(f'Successfully reloaded {cog}')
        except Exception as e:
            self.bot.logger.error(f"Error reloading {cog}: {e}")
            await ctx.send(f'Error reloading {cog}: {e}')

async def setup(bot):
    await bot.add_cog(ReloadCommands(bot))