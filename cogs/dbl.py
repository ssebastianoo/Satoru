import dbl, discord, config
from discord.ext import commands

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = config.tokens.dbl
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))