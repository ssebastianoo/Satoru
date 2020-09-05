import os
import discord
from discord.ext import commands, tasks
from app import keep_alive
import json
import platform
import psutil
from datetime import datetime
import traceback
from dotenv import load_dotenv
from app import keep_alive
import aiohttp

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

def get_prefix(bot, message):

  if message.guild is None:
    prefix = commands.when_mentioned_or("e? ", "e?")(bot, message)
  
  else:
    with open("data/prefixes.json", "r") as f:
      json_prefixes = json.load(f)

    try: 
      oof = str(json_prefixes[str(message.guild.id)])
      prefix = commands.when_mentioned_or(f"{oof} ", oof)(bot, message)

    except KeyError:
      prefix = commands.when_mentioned_or("e? ", "e?")(bot, message)

  return prefix

bot = commands.AutoShardedBot(command_prefix = get_prefix, description = "Multifunction weeb bot with moderation, fun and more.", case_insensitive = True, allowed_mentions = discord.AllowedMentions(roles = False, everyone = False))
bot.remove_command('help')
bot.load_extension('jishaku')
bot.colour = 0x2F3136
bot.launchtime = datetime.now()
bot.session = aiohttp.ClientSession()

@bot.event
async def on_ready():

  print('Ready as', bot.user)

  await bot.change_presence(status = discord.Status.idle, activity = discord.Streaming(name = "e?help", url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

@bot.event
async def on_command_error(ctx, error):

  emb = discord.Embed(title = "Error", description = f"```css\n{error}\n```\nJoin the [support server](https://discord.gg/w8cbssP) for help.", colour = discord.Colour.red(), timestamp = ctx.message.created_at)
  emb.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)

  if isinstance(error, commands.CommandNotFound):
    return

  if isinstance(error, commands.MissingPermissions):
    if ctx.author.id == 488398758812319745:
      return await ctx.reinvoke()

  if isinstance(error, commands.CommandOnCooldown):
    if ctx.author.id == 488398758812319745:
      return await ctx.reinvoke()

    else:
      return await ctx.send(embed = emb, delete_after = 5)

  if isinstance(error, commands.MaxConcurrencyReached):
    emb = discord.Embed(description = f"```sh\n{error}\n```\nJoin the [support server](https://discord.gg/w8cbssP) for help.", colour = discord.Colour.red())
    return await ctx.send(embed = emb, delete_after = 3)
  await ctx.send(embed = emb)

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

load_dotenv(dotenv_path = ".env")
# keep_alive()
token = os.environ.get('secret')
bot.run(token)
