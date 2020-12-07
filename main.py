import discord, config, os
from discord.ext import commands 
from ext.bot import Bot

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

bot = Bot(command_prefix=commands.when_mentioned_or("e?"))
bot.run(config.tokens.bot)