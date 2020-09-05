import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import json
import aiohttp
import os
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import functools
import humanize
import subprocess
from typing import Union
import utils

colour = 0xbf794b

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases = ["setprefix"], invoke_without_command = True)
    @commands.has_permissions(manage_roles = True)
    async def prefix(self, ctx, *, prefix):

      "Set a custom prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      l[str(ctx.guild.id)] = prefix

      with open("data/prefixes.json", "w") as f:

        json.dump(l, f, indent = 4)

      await ctx.send(f"Prefix for **{ctx.guild.name}** set to `{prefix}`.")

    @prefix.command()
    async def reset(self, ctx):

      "Reset the default prefix"

      with open("data/prefixes.json", "r") as f:

        l = json.load(f)

      try:
        
        l.pop(str(ctx.guild.id))

        with open("data/prefixes.json", "w") as f:

          json.dump(l, f)

        await ctx.send(f"Prefix reset to `e?`.")

      except KeyError:

        await ctx.send("Prefix is already the default one (`e?`).")


    @commands.command(aliases = ["info", "ui"])
    async def userinfo(self, ctx, *, member: discord.Member = None):

      "See a member's info"

      member = member or ctx.author
        
      profile = member.public_flags
      badges = ""

      if profile.staff:
        badges += "<:staff:730900251229028352> "

      if profile.verified_bot:
        badges += "<:verified:730900950922952795> "

      if profile.verified_bot_developer:
        badges += "<:botdev:730899790749106176> "

      if profile.partner:
        badges += "<:partner:730900660161347656> "

      if profile.bug_hunter:
        badges += "<:bughunter:730899954683609170> "

      if profile.bug_hunter_level_2:
        badges += "<:bughunter2:730900018873237535> "

      if profile.early_supporter:
        badges += "<:earlysupporter:730900519329071245> "

      if profile.hypesquad_balance:
        badges += "<:HPbalance:730897716938407977> "

      if profile.hypesquad_bravery:
        badges += "<:HPbravery:730897993904947311> "

      if profile.hypesquad_brilliance:
        badges += "<:HPbrilliance:730898410248601760> "

      shared = len([a for a in self.bot.guilds if member.id in [b.id for b in a.members]])

      oof = sorted(ctx.guild.members, key=lambda m: m.joined_at)
      pos = int(oof.index(member)) + 1
      pos = humanize.intcomma(pos)

      if member.nick:
        nick = f"😄 | {member.nick}"

      else: 
        nick = "~~😄 | No Nickname~~"

      if member.activity:
        act = f"🎮 | {member.activity.name}"

      else: 
        act = "~~🎮 | No Activity~~"

      roles = ""

      if member.premium_since:
        booster = f"🎆 | Booster since {member.premium_since.strftime('%m / %d / %Y (%H:%M)')}"

      else:
        booster = "~~🎆 | Not a Booster~~"

      for a in member.roles:

        if a.name == "@everyone":

          roles += "@everyone "

        else:

          roles += f"{a.mention} "

      if member.bot:

        bot = "🤖 | Bot"

      else:

        bot = "~~🤖 | Not a Bot~~"

      if member.is_on_mobile():

        mobile = "📱 | Last seen on Mobile"

      else:

        mobile = "🖥️ | Last seen on Computer"

      emb = discord.Embed(title = member.name, description = f"""
{badges}

😀 | {member.name}
🔢 | {member.discriminator}
🆔 | {member.id}
{nick}
{bot}
{booster}

{act}
🤍 | {member.status}
{mobile}

🍰 | Created at **{member.created_at.strftime("%d %b %Y")} ({humanize.naturaltime(member.created_at)})**
➡️ | Joined at **{member.joined_at.strftime("%d %b %Y")} ({humanize.naturaltime(member.joined_at)})**
<:member_join:596576726163914752> | Joined Position: **{pos}**
➕ | **{shared}** Server(s) shared.

📜 | {roles}""",colour = member.colour, timestamp = ctx.message.created_at)
      emb.set_thumbnail(url = member.avatar_url)
      emb.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["ri"])
    async def roleinfo(self, ctx, *, role: discord.Role):

      "See a role info"

      if role.hoist:

        hoist = f"📲 | Is Hoist"

      else:

        hoist = f"~~📲 | Isn't Hoist~~"

      if role.managed:

        managed = f"⌨️ | Is Managed"

      else: 

        managed = f"~~⌨️ | Isn't Managed~~"

      if role.mentionable:

        mentionable = f"🏓 | Is Mentionable"
      
      else:

        mentionable = f"~~🏓 | Isn't Mentionable~~"

      if role.is_default():

        default = f"📐 | By Default"

      else:

        default = "~~📐 | Not By Default~~"

      emb = discord.Embed(title = role.name, description = f"""
😀  | {role.name}
🆔 | {role.id}
📢 | {role.mention}

🍰 | Created at **{role.created_at.strftime("%d %b %Y")} ({humanize.naturaltime(role.created_at)})**
🙅 | {len(role.members)} users
📑 | {role.position}° position
🎨 | {role.colour}

🛑 | {role.permissions.value} Perms Value
{hoist}
{managed}
{mentionable}
{default}
""", colour = role.colour, timestamp = ctx.message.created_at)
      emb.set_footer(text = ctx.guild.name, icon_url = ctx.guild.icon_url)
      await ctx.send(embed = emb)

    @commands.command(aliases = ["gi", "server", "serverinfo", "si"])
    async def guildinfo(self, ctx, guild_id = None):

      "See the actual guild info"

      if not guild_id:
        
        guild = ctx.guild

      else:

        guild = self.bot.get_guild(guild_id)

      if guild.afk_channel:

        afk = f"💤 | {guild.afk_channel}"

      else:

        afk = "~~💤 | No Afk Channel~~"

      roles = sorted([a for a in guild.roles if a.name != "@everyone"], reverse = True)
      
      roles_ = ""
      counter = 0
      for a in roles:
        if counter < 5:
          roles_ += f"{a.mention} "
          counter += 1

      if not guild.unavailable:

        unav = "🔒 | Is Available"
      
      else: 

        unav = "~~🔒 | Isn't Available~~"

      res = ""

      for a in guild.features:
          
          res += f"{a}, "

      if guild.features:

        features = f"🍔 | {res}"

      else:

        features = "~~🍔 | No Features~~"

      if guild.premium_tier > 0:

        level = f"🎆 | {guild.premium_tier} Nitro Boost Level "

      else:

        level = "~~🎆 | No Booster Level~~"

      if guild.premium_subscription_count > 0:

        boosters = f"💢 | {guild.premium_subscription_count} Boosts"

      else:

        boosters = "~~💢 | No Boosts~~"

      emojis = ""

      for a in guild.emojis:

        emojis += f"{a} "

      online = sum(m.status == discord.Status.online and not m.bot for m in ctx.guild.members)

      dnd = sum(m.status == discord.Status.dnd and not m.bot for m in ctx.guild.members)

      idle = sum(m.status == discord.Status.idle and not m.bot for m in ctx.guild.members)

      offline = sum(m.status == discord.Status.offline and not m.bot for m in ctx.guild.members)

      bots = sum(m.bot for m in ctx.guild.members)
      
      emb = discord.Embed(timestamp = ctx.message.created_at, title = guild.name, description = f"""😀  | {guild.name}
🆔 | {guild.id}
🗺️ | {guild.region}
👤 | {guild.owner.mention} ({guild.owner})
🍰 | Created at **{guild.created_at.strftime("%d %b %Y")} ({humanize.naturaltime(guild.created_at)})**

😴 | {guild.afk_timeout} Seconds
{afk}
{unav}
👮 | {guild.verification_level} 
{features}
{level}

{boosters}
👥 | {guild.member_count} Members
👤 | {len([member for member in ctx.guild.members if not member.bot])} Members
<:status_online:596576749790429200> | {online} Members
<:status_dnd:596576774364856321> | {dnd} Members
<:status_idle:596576773488115722> | {idle} Members
<:status_offline:596576752013279242> | {offline} Members
🤖 | {bots} Bots

📜 | **[Top 5 roles]** {roles_}""", colour = ctx.author.colour)
      emb.set_thumbnail(url = guild.icon_url)
      emb.set_footer(text = guild.name, icon_url = guild.icon_url)

      if guild.banner:

        emb.set_image(url = guild.banner_url)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["userstats"])
    async def users(self, ctx):

      "See users stats"

      async with ctx.typing():

        members = len([x for x in ctx.guild.members if not x.bot])
        online = len([x for x in ctx.guild.members if x.status == discord.Status.online and not x.bot])
        dnd = len([x for x in ctx.guild.members if x.status == discord.Status.dnd and not x.bot])
        idle = len([x for x in ctx.guild.members if x.status == discord.Status.idle and not x.bot])
        offline = len([x for x in ctx.guild.members if x.status == discord.Status.offline and not x.bot])

        members_b = len([x for x in ctx.guild.members if x.bot])
        online_b = len([x for x in ctx.guild.members if x.status == discord.Status.online and x.bot])
        dnd_b = len([x for x in ctx.guild.members if x.status == discord.Status.dnd and x.bot])
        idle_b = len([x for x in ctx.guild.members if x.status == discord.Status.idle and x.bot])
        offline_b = len([x for x in ctx.guild.members if x.status == discord.Status.offline and x.bot])

        online_t = len([x for x in ctx.guild.members if x.status == discord.Status.online])
        dnd_t = len([x for x in ctx.guild.members if x.status == discord.Status.dnd])
        idle_t = len([x for x in ctx.guild.members if x.status == discord.Status.idle])
        offline_t = len([x for x in ctx.guild.members if x.status == discord.Status.offline])

        stats = f"""
------  ALL   ------

Total    ::   {ctx.guild.member_count}
Online   ::   {online_t}
Dnd      ::   {dnd_t}
Idle     ::   {idle_t}
Offline  ::   {offline_t}

------ HUMANS ------

Total    ::   {members}
Online   ::   {online}
Dnd      ::   {dnd}
Idle     ::   {idle}
Offline  ::   {offline}

------  BOTS  ------

Total    ::   {members_b}
Online   ::   {online_b}
Dnd      ::   {dnd_b}
Idle     ::   {idle_b}
Offline  ::   {offline_b}
"""


      emb = discord.Embed(description = f"```prolog\n{stats}\n```", colour = discord.Colour.blurple())

      await ctx.send(embed = emb)

    
    @commands.command(aliases = ["ae"])
    @commands.has_permissions(manage_emojis = True)
    async def addemoji(self, ctx, name = None, emoji_link = None):

      "Add an emoji"

      if not emoji_link:
        
        async with aiohttp.ClientSession() as ses:

          if not ctx.message.attachments:
            emb = discord.Embed(description = f"<:redtick:726040662411313204> | {ctx.author.mention} pls add an attachment to the message or pass a link of an image!", colour = discord.Colour.red())
            return await ctx.send(embed = emb)

          for a in ctx.message.attachments:
            link = a.url
          
          res = await ses.get(link)
          img = await res.read()
          
          await ctx.guild.create_custom_emoji(name = name, image = img, reason = f"Emoji added by {ctx.author}")
          await ctx.send("Done!")

      else:
        
        async with aiohttp.ClientSession() as ses:
          
          res = await ses.get(emoji_link)
          img = await res.read()
          
          await ctx.guild.create_custom_emoji(name = name, image = img, reason = f"Emoji added by {ctx.author}")
          await ctx.send("Done!")

    @commands.command(aliases = ["av", "prfp", "propic"])
    async def avatar(self, ctx, *, member: Union[discord.Member, str] = None):

      "See a member avatar via file"

      async with ctx.typing():

        if not member:
          member = ctx.author

        if type(member) == str:
          if not member.startswith("^"):
            raise commands.CommandError(f'Member "{member}" not found')
          messages = await ctx.channel.history(limit=2).flatten()
          if len(messages) >= 1:
            member = messages[1].author
          
          else:
            raise commands.CommandError("No member up there!")

        try:
          ext = 'gif' if member.is_avatar_animated() else 'png'
          await ctx.send(file=discord.File(io.BytesIO(await member.avatar_url.read()), f"{member.display_name}.{ext}"))
        
        except:
          emb = discord.Embed(colour = member.colour)
          emb.set_image(url =  str(member.avatar_url_as(static_format = "png")))
          emb.set_footer(text = member.display_name, icon_url = member.guild.icon_url)
          await ctx.send(embed = emb)

    @commands.command(aliases = ["cf"])
    async def createfile(self, ctx, name, *, text):

      "Create a file"

      async with ctx.typing():

        if name in os.listdir():

          name = f"{ctx.author.name}-{name}"

        f = open(name,"w+")
        f.write(text)

        file = discord.File(name)

      f.close()

      await ctx.send(file = file)

      os.remove(name)

    @commands.command()
    @commands.max_concurrency(1, BucketType.channel)
    async def top(self, ctx, limit = 500, *, channel: discord.TextChannel = None):

      "See a list of top users in a channel"

      msg1 = await ctx.send("Loading messages...")

      async with ctx.typing():
      
        if not channel: channel = ctx.channel 

        if limit > 1000:

          limit = 1000
      
        res = {} 
        ch = await channel.history(limit = limit).flatten() 
      
        for a in ch:
          if not a.author.bot:
            res[a.author] = {'messages': len([b for b in ch if b.author.id == a.author.id])}
           
        lb = sorted(res, key=lambda x : res[x].get('messages', 0), reverse=True)
        
        oof = ""

        counter = 0
        
        for a in lb:

          counter += 1

          if counter > 10:

            pass

          else:
            
            oof += f"{str(a):<20} :: {res[a]['messages']}\n"

        prolog = f"""```prolog
{'User':<20} :: Messages

{oof}
```
"""
        emb = discord.Embed(description = f"Top {channel.mention} users (last {limit} messages): {prolog}", colour = discord.Color.blurple())

      await ctx.send(embed = emb)
      await msg1.delete()

    @commands.command(aliases = ["inviteinfo", "ii"], hidden = True)
    async def infoinvite(self, ctx, invite: discord.Invite):

      res = f"""
**Server**: {invite.guild.name}
**Code**: {invite.code}
**Uses**: {invite.uses}
**Creator**: {invite.inviter}
**Max Age**: {invite.max_age}
"""
#**Created**: {invite.created_at.strftime('%d %b %Y (%X)')}
      await ctx.send(res)
      

    @commands.command(name = "youtube", aliases = ["yt"])
    @commands.max_concurrency(1, per=BucketType.default, wait=False)
    async def _youtube(self, ctx, *, query):

      "Search a video on YouTube"

      loading = str(self.bot.get_emoji(625409860053237770))
      emb = discord.Embed(description = f"{loading} | Searching **{query}**", colour = 0xffaa2b)
      msg = await ctx.send(embed = emb)

      url = await utils.youtube(query, ctx.author.id, self.bot.loop)

      if not url:
        emb.description = f"<:redTick:596576672149667840> | I can't find **{query}**!"
        emb.colour = discord.Color.red()
        return await msg.edit(embed = emb)

      await msg.edit(content = url, embed = None)
      
    @commands.command()
    async def spotify(self, ctx, *, member: discord.Member = None):
      
      "See Spotify activity of a member"
      
      member = member or ctx.author 

      error = discord.Embed(description = f"<:redTick:596576672149667840> | I can't find any **Spotify** activity!", colour = discord.Colour.red())
  
      if not member.activity:
        return await ctx.send(embed = error)
       
      for a in member.activities:
        if a.name == "Spotify":
          if a.type == discord.ActivityType.listening:
            title = a.title
            image = a.album_cover_url
            try:
              duration = str(a.duration)[:-7]
            except:
              pass
            url = "https://open.spotify.com/track/" + a.track_id
            colour = a.colour
            artists = " | ".join(a.artists)
            album = a.album

            emb = discord.Embed(colour = colour)
            emb.add_field(name = "Title", value = f"[{title}]({url})", inline = False)
            emb.add_field(name = "Artist(s)", value = artists, inline = False)
            emb.add_field(name = "Album", value = album, inline = False)

            if duration:
              emb.add_field(name = "Duration", value = duration, inline = False)

            emb.set_image(url = image)
            emb.set_author(name = member, icon_url = member.avatar_url, url = url)
            return await ctx.send(embed = emb)
         
      await ctx.send(embed = error) 
      
    @commands.command()
    @commands.cooldown(1,5,BucketType.user)
    async def search(self, ctx, *, query):

      "Search a user, a role or an emoji in the server with the flags --user, --role, --emoji"
      
      query = query.split(" --")

      if len(query) == 1:
        type = "user"

      else:
        type = query[1]

      text = str(query[0])

      
      if type.lower() == "user":
        res = [a for a in ctx.guild.members if text.lower() in a.display_name.lower() or text.lower() in str(a).lower() or text.lower() in str(a.id)]
        try:
          res_ = ""
          for a in res:

            perms = ctx.channel.permissions_for(a)
            badges = ""
            
            if a.bot:
              badges += "<:bot_tag:596576775555776522>"

            if ctx.guild.owner == a:
              badges += "<:serverowner:714472902241550378>"

            if perms.manage_messages is True:
              badges += "<:ModHammer:714479952552001536>"
              
            if a.premium_since:
              badges += "<a:booster:714618072153063524>" 

            if a.status == discord.Status.online:
              badges += "<:online:682418179137339393>"

            if a.status == discord.Status.dnd:
              badges += "<:dnd:725470341107023984>"

            if a.status == discord.Status.idle:
              badges += "<:idle:683631216221880376>"
            
            if a.status == discord.Status.offline:
              badges += "<:offline:682418285152698379>"
              
            if a.nick:
              res_ += f"**`{str(a)}`**{badges} (**{a.nick}**)\n"

            else:
              res_ += f"**`{str(a)}`**{badges}\n"

          emb = discord.Embed(description = res_, colour = self.bot.colour)
          emb.set_footer(text = f"Users with \"{text}\" keyword.")
          await ctx.send(embed = emb)
        except:
          res_ = ""
          for a in res:
            if a.nick:
              res_ += f"{str(a)} ({a.nick})\n"
            else:
              res_ += f"{str(a)}\n"
          text = await utils.mystbin(res_)
          await ctx.send(f"**{ctx.author.mention} result was too long, I uploaded it here:**\n- {text}")
        
      if type.lower() == "role":
        res = [a for a in ctx.guild.roles if text.lower() in a.name.lower() or text.lower() in str(a.id) or text.lower() in str(a.colour).lower()]
        try:
          res_ = ""

          for a in res:

            perms = a.permissions
            badges = ""
            if perms.manage_messages is True or perms.administrator is True:
              badges += "<:ModHammer:714479952552001536>"
            res_ += f"{a.mention} {badges}\n"

          emb = discord.Embed(description = res_, colour = self.bot.colour)
          emb.set_footer(text = f"Roles with \"{text}\" keyword.")
          await ctx.send(embed = emb)
        except:
          res_ = ""
          for a in res:
            res_ += f"{a.mention}\n"
          text = await utils.mystbin(res_)
          await ctx.send(f"**{ctx.author.mention} result was too long, I uploaded it here:**\n- {text}")

      if type.lower() == "emoji":
        res = [a for a in ctx.guild.emojis if text.lower() in a.name.lower() or text.lower() in str(a.id)]
        try:
          res_ = ""

          for a in res:
            res_ += f"{a} `{a.name}`\n"

          emb = discord.Embed(description = res_, colour = self.bot.colour)
          emb.set_footer(text = f"Emojis with \"{text}\" keyword.")
          await ctx.send(embed = emb)
        except:
          res_ = ""
          for a in res:
            res_ += f"{a}\n"
          text = await utils.mystbin(res_)
          await ctx.send(f"**{ctx.author.mention} result was too long, I uploaded it here:**\n- {text}")
  
def setup(bot):
    bot.add_cog(Utility(bot))