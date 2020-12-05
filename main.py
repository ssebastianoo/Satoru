import discord, config
from discord.ext import commands 
from ext.bot import Bot

bot = Bot(command_prefix=commands.when_mentioned_or("e?"))
bot.run(config.tokens.bot)