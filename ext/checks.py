from discord.ext import commands

def is_dbi(self):
    async def predicate(self, ctx):
        return ctx.guild.id == 611322575674671107
    return commands.check(predicate)