import discord
from discord.ext import commands
import asyncio
import random
import json
from discord.ext.commands.cooldowns import BucketType
import os
import traceback

colour = 0xbf794b

class Battle(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    self.hg_playing = []

  @commands.command()
  @commands.max_concurrency(1, BucketType.channel)
  async def gun(self, ctx):

    "Make a gun battle"

    l = {}

    emb = discord.Embed(description = "Who react with :gun: more times wins!", colour = discord.Colour.green())
    msg = await ctx.send(embed = emb)

    await msg.add_reaction("🔫")

    def check(reaction, user):

      if user.bot:
        return False

      if reaction.message.id != msg.id:
        return False

      if str(reaction.emoji) == "🔫":
        try:
          l[str(user.id)] += 1

        except KeyError:
          l[str(user.id)] = 1
      
      return False

    try:
      reaction, user = await self.bot.wait_for('reaction_add', check = check, timeout = 10)
    
    except asyncio.TimeoutError:
      lb = sorted(l, key=lambda x : l[x], reverse=True)
      counter = 0

      res = ""

      for a in lb:
        counter += 1
        res += f"\n`{counter}.` <@{a}> - {l[a]} 🔫"

      if len(res) == 0:
        res = "nobody played :("

      emb.description = res
      await msg.edit(embed = emb)

  @commands.command(aliases = ["hungergame", "hg"])
  async def hungergames(self, ctx, *, members = None):

    "Create an Hunger Game! If members is none, bot will choose 8 random members. Use `|` to separate players, Ex. `hungergames lmao | lel | lol....`"

    # 1 --
    #     |---
    # 2 --    |
    #         |----             I spent like 30 mins
    # 3 --    |    |            only for this shitty
    #     |---     |            comment, lmao.
    # 4 --         |         
    #              |----- 0       
    # 5 --         |
    #     |---     |
    # 6 --    |    |
    #         |--- 
    # 7 --    |
    #     |---
    # 8 --

    if not ctx.channel.id in self.hg_playing:

      pass

    else:

      return await ctx.send("I'm already playing a game in this channel!", delete_after = 5)

    self.hg_playing.append(ctx.channel.id)

    if members:

      x = members.split(" | ")

    else:

      x = ctx.guild.members

    try:

      players = random.sample(x, 8)

    except ValueError:

      self.hg_playing.remove(ctx.channel.id)
      return await ctx.send("Min 8 players!")
    
    emb = discord.Embed(colour = discord.Colour.blurple(), title = "Hunger Games")

    emb.description = f"""
**{players[0]}** 
`----- VS -----`     
**{players[1]}**  
                
**{players[2]}**
`----- VS -----`
**{players[3]}**
                
**{players[4]}**
`----- VS -----`     
**{players[5]}**    
                
**{players[6]}**
`----- VS -----`    
**{players[7]}**     
"""

    msg = await ctx.send(embed = emb)

    await asyncio.sleep(2)

    onevtwo = random.choice([players[0], players[1]])
    threevfour = random.choice([players[2], players[3]])
    fivevsix = random.choice([players[4], players[5]])
    sevenveight = random.choice([players[6], players[7]])

    emb.description = f"""
**{onevtwo}**     
`----- VS -----`          
**{threevfour}**        
              
**{fivevsix}**
`----- VS -----`   
**{sevenveight}**
"""

    await msg.edit(embed = emb)
    await asyncio.sleep(2)

    onevthree = random.choice([onevtwo, threevfour])
    fivevseven = random.choice([fivevsix, sevenveight])

    emb.description = f"""
**{onevthree}**

`----- VS -----`       
                
**{fivevseven}**
"""
    await msg.edit(embed = emb)

    await asyncio.sleep(2)

    winner = random.choice([onevthree, fivevseven])

    emb.description = f"""
**👑 {winner} 👑**
"""
    await msg.edit(embed = emb)
    
    self.hg_playing.remove(ctx.channel.id)
    
  @commands.command()
  async def milk(self, ctx):
    "milk."
    await ctx.send(":milk:")

def setup(bot):
    bot.add_cog(Battle(bot))