import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import json
from datetime import datetime

colour = 0xbf794b

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_join(self, guild):

    ch = self.bot.get_channel(607358470907494420)

    emb = discord.Embed(description = f"""<:member_join:596576726163914752> | {self.bot.user.mention} joined **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.green())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    await ch.send(embed = emb)

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):

    ch = self.bot.get_channel(607358470907494420)

    emb = discord.Embed(description = f"""<:leave:694103681272119346> | {self.bot.user.mention} left **{guild.name}**!
🆔 | {guild.id}
👤 | {guild.owner}
🔢 | {guild.member_count} Members
🍰 | Created at {guild.created_at.strftime("%m / %d / %Y (%H:%M)")}""", colour = discord.Colour.red())
    emb.set_footer(text = f"{len(self.bot.guilds)} guilds", icon_url = self.bot.user.avatar_url)
    emb.set_thumbnail(url = guild.icon_url)
    if guild.banner:
      emb.set_image(url = guild.banner_url)
      
    await ch.send(embed = emb)

  @commands.Cog.listener()
  async def on_member_join(self, member):

    guild = member.guild
    channel = self.bot.get_channel(578550625638285332)

    if guild.id == 578548442687864832:

      await channel.send(f"<:join:694105538316992532> {member.mention} ({member}) joined!")

  @commands.Cog.listener()
  async def on_member_remove(self, member):

    guild = member.guild
    channel = self.bot.get_channel(578550625638285332)

    if guild.id == 578548442687864832:

      await channel.send(f"<:leave:694103681272119346> {member.mention} ({member}) left...")

  @commands.Cog.listener()
  async def on_message_edit(self, after, before):

    if before.author == self.bot.user:
      return 
      
    await self.bot.process_commands(before)

def setup(bot):
  bot.add_cog(Events(bot))