import discord, aiosqlite, aiohttp, json
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from datetime import datetime

colour = 0xbf794b

class Events(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.bot.add_check(self.blacklist)

  async def blacklist(self, ctx):
    async with aiosqlite.connect("data/db.db") as db:
      data = await db.execute(f"SELECT * from blacklist where user = {ctx.author.id}")
      data = await data.fetchall()

      if len(data) == 1:
        emb = discord.Embed(description = f"<a:fail:727212831782731796> | {ctx.author.mention} you can't use the bot because you are blacklisted!", colour = self.bot.colour)
        await ctx.send(embed = emb, delete_after = 5)
        return False

      else:
        return True
  
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
  async def on_message(self, message):

    if not message.guild:
      if message.author == self.bot.user:
        return

      async with message.channel.typing():
        message_ = message.content.replace(" ", "%20").replace("!", "%21").replace('"', "%22").replace("#", "%23").replace('$', "%24").replace('%', "%25").replace('&', "%26").replace("'",  "%27")
        async with aiohttp.ClientSession() as cs:
          r = await cs.get(f"https://some-random-api.ml/chatbot?message={message_}")
          r = await r.json()
          
        await cs.close()
        emb = discord.Embed(description = r["response"], colour = self.bot.colour)
        return await message.channel.send(embed = emb)

    #await self.bot.process_commands(message)
  
  @commands.Cog.listener()
  async def on_message_edit(self, after, before):

    if before.author == self.bot.user:
      return 
      
    await self.bot.process_commands(before)
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):

    emb = discord.Embed(description = f"<:bahrooscreaming:676018783332073472> • **{ctx.author}** error!\n<a:fail:727212831782731796> • {error}\n<:notlikeduck:701504231269597214> • Join the [support server](https://discord.gg/w8cbssP) for more help", colour = self.bot.colour)
    if isinstance(error, commands.CommandNotFound):
      return

    elif isinstance(error, commands.CheckFailure):
      return

    if isinstance(error, commands.MissingPermissions):
      if ctx.author.id == 488398758812319745:
        return await ctx.reinvoke()

      else:
        pass

    if isinstance(error, commands.CommandOnCooldown):
      if ctx.author.id == 488398758812319745:
        return await ctx.reinvoke()

      else:
        return await ctx.send(embed = emb, delete_after = 5)

    if isinstance(error, commands.MaxConcurrencyReached):
      emb = discord.Embed(description = f"```sh\n{error}\n```\nJoin the [support server](https://discord.gg/w8cbssP) for help.", colour = discord.Colour.red())
      return await ctx.send(embed = emb, delete_after = 3)

    await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(Events(bot))