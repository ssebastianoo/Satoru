import discord, config, os, config
from discord.ext import commands 
from ext.bot import Bot

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
os.environ["JISHAKU_HIDE"] = "True"

def get_prefix(bot, message):
    if message.author.id == bot.owner_id:
        return commands.when_mentioned_or(f"{config.prefix} ", config.prefix, None)(bot, message)
    else:
        return commands.when_mentioned_or(f"{config.prefix} ", config.prefix)(bot, message)

bot = Bot(command_prefix=get_prefix)
bot.run(config.tokens.bot)