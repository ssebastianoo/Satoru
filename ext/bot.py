import os
from discord.ext import commands 

class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)

    async def on_ready(self):
        print("ready as", self.user)

        #for cog in os.listdir("./cogs"):
         #   if cog.endswith(".py"):
          #      self.load_extension(cog[:-3])