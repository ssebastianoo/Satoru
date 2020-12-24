import discord, os, aiosqlite
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
        await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="memes"))
        connection = await aiosqlite.connect("data/db.db")
        self.cursor = await connection.cursor()
        await self.cursor.execute("CREATE table if not exists trees (user id, trees id)")
        print("ready as", self.user)