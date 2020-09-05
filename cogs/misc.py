import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import aiohttp
import json
import random
import asyncio
from googletrans import Translator
from datetime import datetime
import psutil
import platform
import random
import pytz
import traceback
import time
import praw
from dotenv import load_dotenv
import os
import io
from io import BytesIO
import inspect
import dbl
import humanize
import aiosqlite
import utils

load_dotenv(dotenv_path = ".env")

translator = Translator()

colour = 0xfffca6

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dbl_t = os.environ.get("dbltoken")
        self.dbl = dbl.DBLClient(self.bot, self.dbl_t) 

    @commands.command()
    async def ping(self, ctx):

      "See bot latency"

      start = time.perf_counter()

      msg = await ctx.send(f"Ping...")

      end = time.perf_counter()
      duration = (end - start) * 1000

      pong = round(self.bot.latency * 1000)

      emb = discord.Embed(colour = discord.Colour.blurple(), description = f"""
```prolog
Latency  :: {pong}ms
Response :: {duration:.2f}ms
```""", timestamp = ctx.message.created_at, title = ":ping_pong: | Pong!")

      await msg.edit(embed = emb, content = None)

    @commands.command(aliases = ["ut"])
    async def uptime(self, ctx):

      "See bot uptime"

      uptime = datetime.now() - self.bot.launchtime
      hours, remainder = divmod(int(uptime.total_seconds()), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)

      emb = discord.Embed(description = f':clock: | {days}d {hours}h {minutes}m {seconds}s ({humanize.naturaltime(self.bot.launchtime)})', colour = colour)

      await ctx.send(embed = emb)

    @commands.command()
    async def meme(self, ctx):
      
      "Get a random meme"

      async with ctx.typing():
        
        emb = discord.Embed(colour = 0x2F3136)

        try:
          end = False
          sub = random.choice(["memes", "meme", "dankmemes", "me_irl"])
          async with aiohttp.ClientSession() as cs:
            r_ = await cs.get(f"https://www.reddit.com/r/{sub}/hot.json")
            meme = await r_.json()

          await cs.close()
          while not end:
            r = int(random.choice(range(1, 24)))
            if meme["data"]["children"][r]["data"]["is_self"] == False:
              url = meme["data"]["children"][r]["data"]["url_overridden_by_dest"]
              title = meme["data"]["children"][r]["data"]["title"]
              ups = meme["data"]["children"][r]["data"]["ups"]
              author = "u/" + meme["data"]["children"][r]["data"]["author"]
              subreddit = "r/" + meme["data"]["children"][r]["data"]["subreddit"]
              end = True 

            else:
              end = False

          emb.title = title
          emb.description = f"<a:upvote:639355848031993867> | {ups}"
          emb.url = url
          emb.set_author(name = author, url = f"https://reddit.com/{author}")
          emb.set_image(url = url)
          emb.set_footer(text = subreddit)

        except Exception as e:
          traceback.print_exc()
          return await ctx.send(e)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["fb"])
    async def feedback(self, ctx, *, feedback):

      "Send a feedback to the bot or suggest a new command"

      c = self.bot.get_channel(589546367605669892)

      emb = discord.Embed(title = "New Feedback", colour = colour, description = feedback, timestamp = ctx.message.created_at)
      emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
      
      msg = await c.send(embed = emb)
      await msg.add_reaction("<a:upvote:639355848031993867>")
      await ctx.send("Done!")

    @feedback.error
    async def feedback_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        a = commands.clean_content(use_nicknames = True)
        ctx.prefix = await a.convert(ctx, ctx.prefix)
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}feedback <your feedback>`.", colour = discord.Colour.red())
        return await ctx.send(embed = emb, delete_after = 10) 

    @commands.command()
    async def say(self, ctx, *, message = None):

      "Say something with Satoru"

      if not message:
        if ctx.message.attachments:
          file = await ctx.message.attachments[0].to_file()
          return await ctx.send(file = file)
        else:
          emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}say <your message>`.", colour = discord.Colour.red())
          return await ctx.send(embed = emb, delete_after = 10) 
      if ctx.message.attachments:
        file = await ctx.message.attachments[0].to_file()
      else:
        file = None
      a = commands.clean_content(use_nicknames = True)
      message = await a.convert(ctx, message)

      await ctx.send(message, file = file)

    @say.error
    async def say_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
        a = commands.clean_content(use_nicknames = True)
        ctx.prefix = await a.convert(ctx, ctx.prefix)
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | Wrong usage! Use `{ctx.prefix}say <your message>`.", colour = discord.Colour.red())
        return await ctx.send(embed = emb, delete_after = 10) 
      else:
        await ctx.send(error)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def leave(self, ctx, *, member: discord.Member = None):
      "Fake leave the guild"
      member = member or ctx.author
      
      if member.bot:
        message = member.mention 

      else:
        message = member.display_name

      a = commands.clean_content(use_nicknames = True)
      message = await a.convert(ctx, message)
      
      await ctx.send(f"<:leave:694103681272119346> **{message}** has left **{ctx.guild.name}**")

    @commands.command()
    async def invite(self, ctx, *, bot_: discord.Member = None):
      
      "Invite the bot to your server"
      
      bot_ = bot_ or self.bot.user
      
      if not bot_.bot:
        return await ctx.send("That user is not a bot!")

      if bot_ == self.bot.user:
        invite = discord.utils.oauth_url(bot_.id,permissions = discord.Permissions(permissions = 1479929046), redirect_uri = "https://youtu.be/dQw4w9WgXcQ")
        emb = discord.Embed(title = "Invite Me", colour = self.bot.colour, url = invite)
        return await ctx.send(embed = emb)
      else:
        invite = discord.utils.oauth_url(bot_.id)
       
      await ctx.send(f"<{invite}>")

    @commands.command(aliases = ["stats"])
    async def about(self, ctx):

      "Info about the bot"

      uptime = datetime.now() - self.bot.launchtime
      hours, remainder = divmod(int(uptime.total_seconds()), 3600)
      minutes, seconds = divmod(remainder, 60)
      days, hours = divmod(hours, 24)

      emb = discord.Embed(description = f"""**Developer: `Sebastiano#3151`
Library: `discord.py {discord.__version__}`
Python: `{platform.python_version()}`
Memory: `{psutil.virtual_memory()[2]}%`
CPU: `{psutil.cpu_percent()}%`
Uptime: `{days}d {hours}h {minutes}m {seconds}s ({humanize.naturaltime(self.bot.launchtime)})`
Running on: `{platform.system()}`
Guilds: `{len(self.bot.guilds)}`
Users: `{len(self.bot.users)}`
Invite Link: [Click Me]({discord.utils.oauth_url(self.bot.user.id,permissions = discord.Permissions(permissions = 1479929046), redirect_uri = "https://youtu.be/dQw4w9WgXcQ")})
Support Server: [Click Me](https://discord.gg/w8cbssP)
Top.gg: [Click Me](https://top.gg/bot/635044836830871562)
Vote me: [Click Me](https://top.gg/bot/635044836830871562/vote)
PayPal: [Click Me](https://www.paypal.me/ssebastianoo)
**""", colour = colour)

      await ctx.send(embed = emb)

    @commands.command()
    async def male(self, ctx, thing, member: discord.Member = None):

      "Use this when someone says that a thing is a female but is a male"

      if member:

        res = f"Damnit {member.mention}<:bahrooscreaming:676018783332073472>! {thing} is a **male**!"

      else:

        res = f"Damnit<:bahrooscreaming:676018783332073472>! {thing} is a **male**!"

      emb = discord.Embed(description = res, colour = discord.Colour.red())

      await ctx.send(embed = emb)

    @commands.command()
    async def female(self, ctx, thing, member: discord.Member = None):

      "Use this when someone says that a thing is a male but is a female"


      if member:

        res = f"Damnit {member.mention}<:bahrooscreaming:676018783332073472>! {thing} is a **female**!"

      else:

        res = f"Damnit<:bahrooscreaming:676018783332073472>! {thing} is a **female**!"

      emb = discord.Embed(description = res, colour = discord.Colour.red())

      await ctx.send(embed = emb)

    @commands.command(name = "random")
    async def _random(self, ctx, *elements):

      "Make a random choice"

      emb = discord.Embed(description = random.choice(elements), colour = colour)

      await ctx.send(embed = emb)

    @commands.command(aliases = ["cb"])
    async def codeblock(self, ctx, language, *, code):

      "Transform a code to a codeblock"

      if language == "raw":

        await ctx.send(discord.utils.escape_markdown(f"""```{code}```"""))

      else:
        
        await ctx.send(f"""```{language}\n{code}```""")

    @commands.command(usage = "[top] [bottom]")
    async def drake(self, ctx, *, text):

      "Make the Drake Meme, use \"|\" to separate"

      text = text.split(" | ")

      top = text[0]
      bottom = text[1]

      bottom = bottom.replace('"', " ")

      url = f"https://api.alexflipnote.dev/drake?top={top}&bottom={bottom}"

      url = url.replace(" ", "+")

      async with ctx.typing():
        
        async with aiohttp.ClientSession() as cs:
          
          async with cs.get(url) as r:
            
            res = await r.read()

        await cs.close()
          
        await ctx.send(file = discord.File(io.BytesIO(res), filename="Drake.png"))

    @commands.command(name = "8ball", aliases = ["8b"])
    async def _8ball(self, ctx, *, question):

      "Ask 8ball a question"

      messages = [
        "Sure!",
        "Obvious!",
        "Hell no!",
        "Stars say: \"Dude what the frick, no!\"."
        "Stars say: \"Oh yes dude!\"."
        "Haha, no."
      ]

      emb = discord.Embed(title = question, description = random.choice(messages), colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = ctx.author, icon_url = ctx.author.avatar_url_as(static_format = "png"))

      await ctx.send(embed = emb)

    @commands.command()
    async def raw(self, ctx, *, message):

      "Show a message without markdown"

      try:
        message = ((await ctx.channel.fetch_message(message)).content)

      except:
        message = message
        
      message = discord.utils.escape_mentions(message)
      a = commands.clean_content(fix_channel_mentions = True, escape_markdown = True)
      message0 = await a.convert(ctx, message)
      message1 = discord.utils.escape_markdown(message0)

      emb = discord.Embed(colour = colour)
      emb.add_field(name = "Raw", value = message0, inline = False)
      emb.add_field(name = "Escape Markdown", value = message1, inline = False)

      await ctx.send(embed = emb)

    @commands.command()
    async def messages(self, ctx, limit = 500, channel: discord.TextChannel = None, member: discord.Member = None):

      """See how many messages a member sent in a channel in the last tot messages
Use `messages <limit> <channel> <member>`"""

      if limit > 5000:

        limit = 5000

      if not channel:

        channel = ctx.channel

      if not member:

        member = ctx.author
        
        a = "You"

      else:

        member = member
        a = member.mention

      async with ctx.typing():
        
        messages = await channel.history(limit=limit).flatten()
        count = len([x for x in messages if x.author.id == member.id])
        
        perc = ((100 * int(count))/int(limit))
        
        emb = discord.Embed(description = f"{a} sent **{count} ({perc}%)** messages in {channel.mention} in the last **{limit}** messages.", colour = colour)
        
        await ctx.send(embed = emb)

    @commands.command()
    async def spoiler(self, ctx, *, message):

      "Make a message with a lot of spoilers"

      res = ""

      for a in message:

        res += f"||{a}||"

      await ctx.send(discord.utils.escape_mentions(res))

    async def from_utc(self, timezone):

      local_tz = pytz.timezone(str(timezone))
      
      local_dt = datetime.now().replace(tzinfo=pytz.utc).astimezone(local_tz)

      return local_tz.normalize(local_dt).strftime("%d %b %Y - %I:%M:%S %p")

    @commands.command(aliases = ["tz", "timezones"])
    async def timezone(self, ctx, *, timezone = None):

      "See what time is in a country"

      if not timezone:

        async with ctx.typing():

          rome = await self.from_utc("Europe/Rome")
          paris = await self.from_utc("Europe/Paris")
          tokyo = await self.from_utc("Asia/Tokyo") 
          london = await self.from_utc("Europe/London")
          berlin = await self.from_utc("Europe/Berlin")
          moscow = await self.from_utc("Europe/Moscow")
          toronto = await self.from_utc("America/Toronto")
          detroit = await self.from_utc("America/Detroit")
          shanghai = await self.from_utc("Asia/Shanghai")
          helsinki = await self.from_utc("Europe/Helsinki")
          newyork = await self.from_utc("America/New_York")
          amsterdam = await self.from_utc("Europe/Amsterdam")

          emb = discord.Embed(description = f"""```prolog
Rome       ::   {rome}
Paris      ::   {paris}
Tokyo      ::   {tokyo}
London     ::   {london}
Berlin     ::   {berlin}
Moscow     ::   {moscow}
Toronto    ::   {toronto}
Detroit    ::   {detroit}
Shanghai   ::   {shanghai}
Helsinki   ::   {helsinki}
New York   ::   {newyork}
Amsterdam  ::   {amsterdam}
```""", colour = discord.Colour.blurple())

        return await ctx.send(embed = emb)

      try:
      
        emb = discord.Embed(description = f"```prolog\n{timezone} :: {await self.from_utc(str(timezone))}\n```", colour = discord.Colour.blurple())

        await ctx.send(embed = emb)

      except:

        emb = discord.Embed(description = f"**{timezone}** is not a valid timezone!\n\nUse a format like this: **Europe/Rome**.\n\n[Here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is a list of timezones", colour = discord.Colour.red())

        await ctx.send(embed = emb)

    @commands.command()
    async def poll(self, ctx, poll, *, options = None):

      "Make a poll"

      if not options:

        emb = discord.Embed(title = f"⁉️ | {poll}", colour = discord.Colour.blurple())
        emb.set_footer(text = "Vote")

        msg = await ctx.send(embed = emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

        return

      options = options.split(",")

      if len(options) > 10:

        return await ctx.send("Max 10 options!")

      elif len(options) < 2:

        return await ctx.send("Min 2 options!")

      count = 0

      emojis = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

      res = ""

      for a in options:

        emoji = emojis[int(count)]
        count += 1
        res += f"\n{emoji} - {a}"

      emb = discord.Embed(title = f"⁉️ | {poll}", description = res, colour = discord.Colour.blurple())
      emb.set_footer(text = "Vote")

      msg = await ctx.send(embed = emb)

      for a in emojis[:len(options)]:

        await msg.add_reaction(a)

    @commands.command()
    async def strange(self, ctx, *, message):
      "sTrAnGe"

      clean = commands.clean_content(use_nicknames = True)
      msg = await clean.convert(ctx, message)

      res = ""
      way = "lo"

      for letter in msg:
        if way == "lo":
          res += letter.lower()
          way = "up"

        else:
          res += letter.upper()
          way = "lo"

      await ctx.send(res)

    @commands.command()
    async def clap(self, ctx, *message):
      "clap clap"

      clap = " 👏 ".join(message)
      a = commands.clean_content(use_nicknames = True)
      msg = await a.convert(ctx, clap)

      await ctx.send(f"👏 {msg} 👏")

    @commands.command(aliases = ["src"])
    async def source(self, ctx, *, command):
      "See command source"
        
      cmd = self.bot.get_command(command)
      if not cmd:
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | Command **{command}** not found.", colour = discord.Colour.red())
        return await ctx.send(embed = emb)

      try:
        source_lines, _ = inspect.getsourcelines(cmd.callback)
      except (TypeError, OSError):
        emb = discord.Embed(description = f"<:redTick:596576672149667840> | I can't get **{command}** source.", colour = discord.Colour.red())
        return await ctx.send(embed = emb)

      source_lines_ = ''.join(source_lines)

      url = await utils.mystbin(str(source_lines_))

      await ctx.send(f"{url}.py")

    @commands.command()
    async def vote(self, ctx):

      "Vote the bot on top.gg"

      await ctx.send("https://top.gg/bot/635044836830871562/vote")

    @commands.command(aliases = ["spaces"])
    async def space(self, ctx, *, text):

      "Make a lot of spaces between letters"

      a = commands.clean_content(use_nicknames = True)

      msg = await a.convert(ctx, text)

      message = "  ".join(msg)

      await ctx.send(message)

    @commands.command(aliases = ["doggo"])
    async def dog(self, ctx):

      "Get a random dog picture"

      async with aiohttp.ClientSession() as cs:
        
        async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
          
          res = await r.json()  
          
          url = res["message"]

      await cs.close()

      nick = ctx.author.display_name

      emb = discord.Embed(title = "Doggo", url = url, colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = nick, icon_url = ctx.author.avatar_url)
      emb.set_image(url = url)
      
      await ctx.send(embed = emb)

    @commands.command(aliases = ["catto", "pussy"])
    async def cat(self, ctx):

      "Get a random cat picture"

      async with aiohttp.ClientSession() as cs:
        
        async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
          
          res = await r.json()  # returns dict
          
          url = res[0]['url']

      await cs.close()

      nick = ctx.author.display_name

      emb = discord.Embed(title = "Cat", url = url, colour = colour, timestamp = ctx.message.created_at)
      emb.set_author(name = nick, icon_url = ctx.author.avatar_url)
      emb.set_image(url = url)
      
      await ctx.send(embed = emb)

    @commands.command(aliases = ["player", "activity"])
    async def players(self, ctx, *, game):

      "See how many players are playing a game"

      players = []
      
      for a in ctx.guild.members:
        if a.activity:
          for b in a.activities:
            if b.name:
              if game.lower() == str(b.name.lower()):
                players.append(a)

      if len(players) == 0:
        a = commands.clean_content(use_nicknames = True)
        game = await a.convert(ctx, game)
        return await ctx.send(f"Nobody in **{ctx.guild.name}** has **{game}** in their activities.")

      fin_players = ""
      for a in players:
        fin_players += f"{str(a)}\n"

      fin_players = await utils.mystbin(fin_players)

      emb = discord.Embed(description = f"**{len(players)}** [users]({fin_players}) in **{ctx.guild.name}** have **{game}** in their activities.", colour = colour)
      await ctx.send(embed = emb)

    @commands.command(aliases = ["owo"])
    async def owoify(self, ctx, *, text):
      "OwO"

      text = text.replace(" ", "+")
      text = text.replace("\n", "+")

      a = commands.clean_content(use_nicknames = True)
      text = await a.convert(ctx, text)

      async with aiohttp.ClientSession() as cs:
        r = await cs.get(f"https://nekos.life/api/v2/owoify?text={text}")
        b = await r.json()

      await cs.close()

      await ctx.send(b["owo"])

    @commands.command()
    async def mention(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
      "See who pinged / mentioned a member"
      message = None
      async with ctx.typing():
        member = member or ctx.author
        channel = channel or ctx.channel
        async for a in channel.history(limit=5000):
          if a.id == ctx.message.id:
            pass
          else:
            if member.mention in a.content:
              message = a
              break

        if not message:
          emb = discord.Embed(description = f"<:redTick:596576672149667840> | Last mention is too old or {member.mention} got never mentioned and I can't find it!", colour = discord.Colour.red())
          return await ctx.send(embed = emb, delete_after = 10)

        emb = discord.Embed(description = f"{message.content}\n\n[[Jump]({message.jump_url})]", timestamp = message.created_at, colour = message.author.colour)
        emb.set_author(name = message.author, icon_url = message.author.avatar_url_as(static_format = "png"))

        await ctx.send(embed = emb)

    @commands.command()
    async def binary(self , ctx, *, text):

      text = discord.utils.escape_markdown(text)

      msg = await ctx.send(f"**Choose:\n- 📝 `Binary` to `Text`.\n- 💻 `Text` to `Binary`.**")
      await msg.add_reaction("📝")
      await msg.add_reaction("💻")

      def check(reaction, user):
        return user.id == ctx.author.id and reaction.message.id == msg.id

      end = False

      while not end:

        try:
          msg_ = await self.bot.wait_for("reaction_add", check = check, timeout = 30)
          
        except asyncio.TimeoutError:
          return await ctx.send(f":clock: | {ctx.author.mention} **Timeout**!", delete_after = 60)
          
        if str(msg_[0]) == "💻":
          text = ' '.join(format(ord(x), 'b') for x in text)
          if len(text) >= 680:
            text = await utils.mystbin(text)
            await ctx.send(f"**{ctx.author.mention} text was too long, I uploaded it here:**\n- {text}")
            await msg.delete()
            end = True

          else:
            emb = discord.Embed(description = text, colour = 0x36393E)
            await ctx.send(embed = emb)
            await msg.delete()
            end = True
          
        elif str(msg_[0]) == "📝":
          b = text.split()
          try:
            ascii_string = ""
            for a in b:
              oof = int(a, 2)
              ascii_character = chr(oof)
              ascii_string += ascii_character
          except:
            await ctx.send(f"**{ctx.author.mention} I can't encode it, are you sure that it is a Binary code?**", delete_after = 40)
            return await msg.delete()
          try:
            emb = discord.Embed(description = ascii_string, colour = 0x36393E)
            await ctx.send(embed = emb)
            await msg.delete()
          except:
            text = await utils.mystbin(text)
            await ctx.send(f"**{ctx.author.mention} text was too long, I uploaded it here:**\n- {text}")
            await msg.delete()
          end = True

        else:
          end = False
    
    @commands.command(name = "mystbin")
    @commands.cooldown(1, 10, BucketType.user)
    async def _mystbin(self, ctx, *, text):
      "Upload a text to hastebin"
      link = await utils.mystbin(text)
      await ctx.send(link)

    @commands.command()
    async def support(self, ctx):
      "Support the bot development"
      emb = discord.Embed(description = f"""**Do you want to support Satoru?**

- [Vote the bot](https://top.gg/bot/635044836830871562/vote)

- [Donate something](https://www.paypal.me/ssebastianoo)""", colour = discord.Colour.blurple())
      await ctx.send(embed = emb)

    @commands.command() 
    async def lmgtfy(self, ctx, *, query):
      "Use this when someone ask you something that"

      a = commands.clean_content(use_nicknames = True)
      query = await a.convert(ctx, query)
      query_u = query.replace(" ", "%20")
      query_u = query_u.replace("'", "%27")
      url = f"https://lmgtfy.com/?q={query_u}&iie=1"
      emb = discord.Embed(title = query, url = url, colour = self.bot.colour)
      await ctx.send(embed = emb)

    @commands.group(aliases = ["dbl", "topgg"], invoke_without_command = True)
    async def dblinfo(self, ctx, bot_id):
      if ctx.message.mentions:
        bot_id = ctx.message.mentions[0].id

      try:
        bot_info = await self.dbl.get_bot_info(bot_id)
      except:
        return await ctx.send("Bot not found.")

      page = f"https://top.gg/bot/{bot_info['id']}"
      avatar = f"https://cdn.discordapp.com/avatars/{bot_info['id']}/{bot_info['avatar']}.png?size=1024"
      support = f"https://discord.gg/{bot_info['support']}"
      widget = await self.dbl.get_widget_large(bot_id)

      emb = discord.Embed(description = f"""
{bot_info['shortdesc']}

**Page: [Click Me]({page})
Support Server: [Click Me]({support})
Invite: [Click Me]({bot_info['invite']})
Prefix: `{bot_info['prefix']}`
Tags: `{', '.join(bot_info['tags'])}`
Total Upvotes: `{bot_info['points']}`
Monthly Upvotes: `{bot_info['monthlyPoints']}`**""", colour = discord.Colour.blurple())
      emb.set_author(name = bot_info["username"], url = page, icon_url = avatar)
      emb.set_thumbnail(url = avatar)
      emb.set_image(url = widget)
      await ctx.send(embed = emb)

    @dblinfo.command()
    async def badge(self, ctx, bot_id):
      "See DBL badge of a bot listed on top.gg"
      
      if ctx.message.mentions:
        bot_id = ctx.message.mentions[0].id
      
      try:
        widget = await self.dbl.get_widget_large(bot_id)
      except:
        return await ctx.send("Bot not found.")

      async with self.bot.session.get(widget) as r:
          img = await r.read()

      await ctx.send(file = discord.File(BytesIO(img), filename = f"{bot_id}.png")) 
    
    @commands.command()
    @commands.is_owner()
    @commands.cooldown(1, 10, BucketType.user) 
    async def notify(self, ctx, *, channel: discord.TextChannel = None):
      "Get notified when a channel will return active"

      channel = channel or ctx.channel

      async with aiosqlite.connect("data/notify.db") as db:
        try:
          await db.execute(f"CREATE TABLE '{ctx.guild.id}' ('{ctx.author.id}' int)")
          await db.execute(f"INSERT into '{ctx.guild.id}' ('{ctx.author.id}') VALUES ('{channel.id}')")
        except aiosqlite.OperationalError as e:
          try:
            await db.execute(f"INSERT into '{ctx.guild.id}' ('{ctx.author.id}') VALUES ('{channel.id}')")
          except aiosqlite.OperationalError as e:
            await db.execute(f"ALTER TABLE '{ctx.guild.id}' ADD COLUMN '{ctx.author.id}' int")
            await db.execute(f"INSERT into '{ctx.guild.id}' ('{ctx.author.id}') VALUES ('{channel.id}')")    
        finally:
          await db.commit()    

        await ctx.send("done")

    @commands.command()
    async def bans(self, ctx, limit: int = 10):
      "Check who got banned"

      if limit > 20:
        limit = 20

      bans = []

      emb = discord.Embed(description = "", colour = 0x2F3136)

      async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.ban, limit = limit):
        emb.description += f"[**{humanize.naturaltime(entry.created_at)}**] **{str(entry.user)}** banned **{str(entry.target)}**\n- {entry.reason}\n\n"

      await ctx.send(embed = emb)

    @commands.command()
    async def comment(self, ctx, *, text):
      "Make a (fake) youtube comment"

      async with ctx.typing():
        a = commands.clean_content(use_nicknames = True)
        text = await a.convert(ctx, text)
        text = text.replace("&", "%26")
        url = f"https://some-random-api.ml/canvas/youtube-comment?username={ctx.author.display_name}&avatar={ctx.author.avatar_url_as(format = 'png')})?size=1024&comment={text}"
        url = url.replace(" ", "%20")
        url = url.replace("#", "%23")

        async with self.bot.session.get(url) as r:
          b = await r.read()
          
        await ctx.send(file = discord.File(BytesIO(b), filename = f"{text}.png"), content = "Powered by <https://some-random-api.ml/>")

    @commands.command()
    async def shared(self, ctx, user: discord.User = None):
      "See which servers do I share with a User"

      user = user or ctx.author
      shared = [g.name for g in self.bot.guilds if g.get_member(user.id)]
      s = "servers"

      if len(shared) == 1 or len(shared) ==  0:
        s = "server"

      res = ""
      for a in shared:
        res += f"• {a}\n"

      emb = discord.Embed(description = f"""I share **{len(shared)}** {s} with **{str(user)}**
      
{res}""", colour = 0x2F3136)
      await ctx.send(embed = emb)

    @commands.group(invoke_without_command = True)
    async def roo(self, ctx, roo = None):
      "send a roo emoji, if not specified bot will send a random roo"
      guild = self.bot.get_guild(722499238067437639)
      emojis = [a for a in guild.emojis if a.name.startswith("roo")]
      if not roo:
        await ctx.send(str(random.choice(emojis)))

      else:
        for emoji in emojis:
          if emoji.name.lower() == roo.lower():
            return await ctx.send(str(emoji))
          
          elif roo.lower() in emoji.name.lower():
            return await ctx.send(str(emoji))
        
        return await ctx.send(str(random.choice(emojis)))

    @roo.command()
    async def list(self, ctx):
      "return a list of roo emojis"

      guild = self.bot.get_guild(722499238067437639)
      emojis = [a for a in guild.emojis if a.name.startswith("roo")]

      emb = discord.Embed(description = "\n".join([f"{str(a)} `{a.name}`" for a in emojis]), colour = 0x2F3136)
      await ctx.send(embed = emb)

def setup(bot):
  bot.add_cog(Misc(bot))
