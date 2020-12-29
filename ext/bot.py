import discord, os, aiosqlite, config
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=self.get_prefix, intents=discord.Intents.default())
        self.load_extension("jishaku")
        self.colour = 0x2F3136

        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                self.load_extension(f"cogs.{cog[:-3]}")

    async def get_prefix_(self, bot, message):
        if message.author.id == bot.owner_id:
            prefix = [f"{config.prefix} ", config.prefix, ""]
        else:
            prefix = [f"{config.prefix} ", config.prefix]
        return commands.when_mentioned_or(prefix)(bot, message)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="memes"))
        self.connection = await aiosqlite.connect("data/db.db")
        await self.connection.execute("CREATE table if not exists trees (user id, trees id)")
        print("ready as", self.user)