import discord
from discord.ext import commands
from typing import Union

#COLOUR: 0xbf794b

class Moderation(commands.Cog):

  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases = ["purge"])
  @commands.has_permissions(kick_members = True)
  async def clear(self, ctx, amount = 100, *, user: Union[discord.User, int] = None):
    """Delete Messages"""

    if user:
      if type(user) == int:
        def check(m):
          return m.author.id == user

      else:
        def check(m):
          return m.author.id == user.id

    else:
      def check(m):
        return True
    
    await ctx.message.delete()
    await ctx.channel.purge(limit = amount, check = check)

  @commands.group(invoke_without_command = True)
  @commands.has_permissions(ban_members = True)
  async def ban(self, ctx, member: discord.Member = None, *, reason = None):

    "Ban a member"

    await member.ban(reason = reason, delete_message_days = 2)

    emb = discord.Embed(description = f"✅ | {member.mention} has been banned by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

  @ban.command(aliases = ["force", "super", "id"])
  @commands.has_permissions(ban_members = True)
  async def sudo(self, ctx, user_id: int, *, reason = None):

    "Ban a user that is not in the actual guild"

    await ctx.guild.ban(discord.Object(id = user_id), reason = reason, delete_message_days = 2)

    emb = discord.Embed(description = f"✅ | <@{user_id}> ({user_id}) has been banned by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, user_id: int):

    "Unban a user"

    await ctx.guild.unban(discord.Object(id = user_id))

    emb = discord.Embed(description = f"✅ | <@{user_id}> ({user_id}) has been unbanned by {ctx.author.mention}", colour = discord.Colour.green())

    await ctx.send(embed = emb)

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member = None, *, reason = None):

    "Kick a member"

    await member.kick(reason = reason)

    emb = discord.Embed(description = f"✅ | {member.mention} has been kicked by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def mute(self, ctx, member: discord.Member = None, *, reason = None):

    "Mute a member"

    r = discord.utils.get(ctx.guild.roles, name = "Muted")

    if not r:

      r = await ctx.guild.create_role(name = "Muted")

    await member.add_roles(r, reason = reason)

    emb = discord.Embed(description = f"✅ | {member.mention} has been muted by {ctx.author.mention}", colour = discord.Colour.red())

    await ctx.send(embed = emb)

    try:
      
      for a in ctx.guild.channels:
        
        await a.set_permissions(r, send_messages = False)

    except:

      return

  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def unmute(self, ctx, member: discord.Member = None):

    "Unmute a member"

    r = discord.utils.get(ctx.guild.roles, name = "Muted")

    await member.remove_roles(r)

    emb = discord.Embed(description = f"✅ | {member.mention} has been unmuted by {ctx.author.mention}", colour = discord.Colour.green())

    await ctx.send(embed = emb)

  @commands.command()
  async def lock(self, ctx, *, channel: discord.TextChannel = None):

    "Lock a Text Channel"

    if not channel:

      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)

      await ctx.send(f"🔒 | Locked {ctx.channel.mention}.")

    else:

      await channel.set_permissions(ctx.guild.default_role, send_messages = False)

      await ctx.send(f"🔒 | Locked {channel.mention}.")

  @commands.command()
  async def unlock(self, ctx, *, channel: discord.TextChannel = None):

    "Unlock a Text Channel"

    if not channel:

      await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = None)

      await ctx.send(f"🔓 | Unlocked {ctx.channel.mention}.")

    else:

      await channel.set_permissions(ctx.guild.default_role, send_messages = None)

      await ctx.send(f"🔓 | Unlocked {channel.mention}.")

def setup(bot):
  bot.add_cog(Moderation(bot))