import discord
from discord.ext import commands

colour = discord.Colour.blurple()

class Minecraft(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def skin(self, ctx, arg=None):

    "See a skin of player"

    emb = discord.Embed(description = f"{arg}'s Skin", colour = colour)
    emb.set_image(url = f'https://minotar.net/skin/{arg}') 

    await ctx.send(embed = emb)

  @commands.command()
  async def head(self, ctx, arg=None):

    "See the head of a player"

    emb = discord.Embed(description = f"{arg}'s Head", colour = colour)
    emb.set_image(url = f'https://minotar.net/avatar/{arg}/500.png') 

    await ctx.send(embed = emb)

  @commands.command()
  async def helm(self, ctx, arg=None):

    "See the head of a player with the helm (if there is)"

    emb = discord.Embed(description = f"{arg}'s Helm", colour = colour)
    emb.set_image(url = f'https://minotar.net/helm/{arg}/500.png') 

    await ctx.send(embed = emb)

  @commands.command()
  async def cubehead(self, ctx, arg=None):

    "See the head of a player in a 3D way"

    emb = discord.Embed(description = f"{arg}'s Cubehead", colour = colour)
    emb.set_image(url = f'https://minotar.net/cube/{arg}/500.png') 

    await ctx.send(embed = emb)

  @commands.command()
  async def bust(self, ctx, arg=None):

    "See the bust of a player"

    emb = discord.Embed(description = f"{arg}'s Bust", colour = colour)
    emb.set_image(url = f'https://minotar.net/armor/bust/{arg}/500.png') 

    await ctx.send(embed = emb)

  @commands.command()
  async def body(self, ctx, arg=None):

    "See the body of a player"

    emb = discord.Embed(description = f"{arg}'s Body", colour = colour)
    emb.set_image(url = f'https://minotar.net/armor/body/{arg}/500.png') 

    await ctx.send(embed = emb)



def setup(bot):
  bot.add_cog(Minecraft(bot))