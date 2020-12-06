import discord, os
from discord.ext import commands 

class Bot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix, intents=discord.Intents.default())
        self.load_extension("jishaku")
        self.colour = 0x2F3136

        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                self.load_extension(f"cogs.{cog[:-3]}")

    async def on_ready(self):
        print("ready as", self.user)