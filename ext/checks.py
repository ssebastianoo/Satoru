from discord.ext import commands
import config

def is_dbi():
    async def predicate(ctx):
        return ctx.guild.id == config.dbi.id
    return commands.check(predicate)
