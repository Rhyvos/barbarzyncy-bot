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

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """Reloads a cog"""
        await ctx.defer(ephemeral=True)
        try:
            self.bot.unload_extension(f'cogs.{cog}')
            self.bot.load_extension(f'cogs.{cog}')
            await ctx.send(f'Successfully reloaded {cog}')
        except Exception as e:
            await ctx.send(f'Error reloading {cog}: {e}')

def setup(bot):
    bot.add_cog(ReloadCommands(bot))