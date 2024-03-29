import discord
from discord.ext import commands
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CheckFailure):
            if ctx.command.name == "trees":
                return

        if isinstance(error, commands.CommandNotFound):
            return
            
        await ctx.send(f"```{error}```")
    
def setup(bot):
    bot.add_cog(Events(bot))
