import discord, aiosqlite, asyncio, os, json, traceback, io, sys, copy, aiohttp, subprocess, textwrap, aiosqlite
from discord.ext import commands, tasks
from datetime import datetime
from contextlib import redirect_stdout
from utils import Git
from typing import Union

colour = 0xbf794b
#git = Git(self.bot.loop)

class Owner(commands.Cog, command_attrs = dict(hidden = True)):

  def __init__(self, bot):
    self.bot = bot
    self._last_result = None

  def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

  @commands.command()
  async def emoji(self, ctx, emoji: discord.Emoji = None):

    if emoji.animated:
      
      await ctx.send(f'`<a:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

    else:

      await ctx.send(f'`<:{emoji.name}:{emoji.id}>` - {emoji} - {emoji.id} - {emoji.url}')

  @commands.command()
  @commands.is_owner()
  async def load(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Loaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    
    try:
      
      self.bot.load_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except Exception as e:

      traceback.print_exc()

      error = discord.Embed(title = f"""UH! There was an error with {extension}!""", description = str(e), colour = 0xbf794b)
      await msg.edit(embed = error)

  @commands.command()
  @commands.is_owner()
  async def reload(self, ctx, *, extension = None):
    "reload a cog"

    async with ctx.typing():
      #await git.pull()

      if not extension:
        emb = discord.Embed(description = f"<a:loading:747680523459231834> | Reloading all extensions", colour = self.bot.colour)
        msg = await ctx.send(embed = emb)
        emb.description = ""
        
        for cog in os.listdir("./cogs"):
          if cog.endswith(".py"):
            try:
              self.bot.unload_extension(f"cogs.{cog[:-3]}")
              self.bot.load_extension(f"cogs.{cog[:-3]}")
            except:
              emb.description += f"<a:fail:727212831782731796> {cog[:-3]}\n"
            else:
              emb.description += f"<a:check:726040431539912744> {cog[:-3]}\n"

        return await msg.edit(content = None, embed = emb)

      emb = discord.Embed(description = f"<a:loading:747680523459231834> | Reloading {extension}", colour = self.bot.colour)
      msg = await ctx.send(embed = emb)
      
      try:
        self.bot.unload_extension(f"cogs.{extension}")
        self.bot.load_extension(f"cogs.{extension}")
      except Exception as e:
        emb.description = f"<a:fail:727212831782731796> | {extension}\n```bash\n{e}\n```"
      else:
        emb.description = f"<a:check:726040431539912744> {extension}"

      await msg.edit(content = None, embed = emb)
    
  @commands.command()
  @commands.is_owner()
  async def unload(self, ctx, extension):
    emb = discord.Embed(title = 'Loading...', colour = 0xbf794b)
    emb1 = discord.Embed(title = f'Unloaded {extension}!', colour = 0xbf794b)
    msg = await ctx.send(embed = emb)
    await asyncio.sleep(0.5)
    
    try:
      
      self.bot.unload_extension(f'cogs.{extension}')
      
      await msg.edit(embed = emb1)

    except Exception as e:

      traceback.print_exc()

      error = discord.Embed(title = f"""UH! There was an error with {extension}!""", description = str(e), colour = 0xbf794b)
      await msg.edit(embed = error)

  @commands.command()
  @commands.is_owner()
  async def asyncio(self, ctx, time, times = None, *, thing = None):

    "Sleep little Satoru"

    if not times:

      times = 1

    if thing:

      thing = f"**{thing}**"

    else:

      thing = " "

    await ctx.message.add_reaction("\U0001f44d")

    for a in range(int(times)):
      
      await asyncio.sleep(int(time))

    before = ctx.message.created_at
    
    await ctx.send(f"{ctx.author.mention}, at `{before.strftime('%d %b %Y - %I:%M %p')}` {thing}")

  @commands.command()
  @commands.is_owner()
  async def nick(self, ctx, *, nick):

    "Nickname the bot"

    await ctx.guild.me.edit(nick = nick)
    await ctx.message.add_reaction("<:greenTick:596576670815879169>")

  @commands.command(hidden=True)
  @commands.is_owner()
  async def eval(self, ctx, *, body: str):
    """Evaluates a code"""

    env = {
        'bot': self.bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': self._last_result,
        'owner': self.bot.get_user(488398758812319745)
    }

    env.update(globals())

    body = self.cleanup_code(body)

    body = f"import asyncio\nimport aiosqlite\nimport os\nimport aiohttp\nimport random\nimport humanize\n{body}"

    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.message.add_reaction("<:redTick:596576672149667840>")
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('<a:check:707144339444465724>')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(value)
        else:
            self._last_result = ret
            await ctx.send(f'{value}{ret}')

  @commands.command()
  @commands.is_owner()
  async def restart(self, ctx):
    "restart the bot"

    await ctx.message.add_reaction("👋")
    subprocess.call("python3 main.py", shell = True)
    self.bot.close()

  @commands.group(invoke_without_command = True, aliases = ["sql"])
  @commands.is_owner()
  async def sqlite(self, ctx, *, command):
    "run a sqlite command"

    command = eval(f"f'{command}'")
    
    async with aiosqlite.connect("data/db.db") as db:
        data = await db.execute(command)

        if command.lower().startswith("select"):
            data = await data.fetchall()
            emb = discord.Embed(description = f"```py\n{data}\n```", colour = self.bot.colour)
            await ctx.send(embed = emb)

        await db.commit()

    await ctx.message.add_reaction("<a:check:726040431539912744>")

  @commands.command(aliases = ["bl"])
  @commands.is_owner()
  async def blacklist(self, ctx, member: Union[discord.Member, discord.User] = None):
    "blacklist a user"

    async with ctx.typing():
      async with aiosqlite.connect("data/db.db") as db:
        if member:
          await db.execute(f"INSERT into blacklist (user) VALUES ({member.id})")
          await db.commit()

        else:
          data = await db.execute(f"SELECT * from blacklist")
          data = await data.fetchall()

          emb = discord.Embed(description = f"These users are blacklisted:\n", colour = self.bot.colour)
          
          for user in data:

            if int(user[0]) == 0:
              pass

            else:
              u = self.bot.get_user(int(user[0]))
              if not u:
                emb.description += f"• **{user[0]}** (I cannot see this user)\n"

              else:
                emb.description += f"• **{u}**\n"

          return await ctx.send(embed = emb)

      emb = discord.Embed(description = f"<a:check:726040431539912744> | Blacklisted **{member}**", colour = self.bot.colour)
      await ctx.send(embed = emb)
      await ctx.message.add_reaction("<a:check:726040431539912744>")

  @commands.command(aliases = ["ubl"])
  @commands.is_owner()
  async def unblacklist(self, ctx, member: Union[discord.Member, discord.User] = None):
    "blacklist a user"

    async with ctx.typing():
      async with aiosqlite.connect("data/db.db") as db:
          await db.execute(f"UPDATE blacklist set user = 0 where user = {member.id}")
          await db.commit()

      emb = discord.Embed(description = f"<a:check:726040431539912744> | Unblacklisted **{member}**", colour = self.bot.colour)
      await ctx.send(embed = emb)
      await ctx.message.add_reaction("<a:check:726040431539912744>")
      
def setup(bot):
  bot.add_cog(Owner(bot))