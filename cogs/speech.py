import speech_recognition as sr 
import discord
from discord.ext import commands
from io import BytesIO
import aiohttp
import traceback
from aiogtts import aiogTTS
import functools
from tempfile import TemporaryFile
import io

r = sr.Recognizer()

class Speech(commands.Cog):
  def __init__(self, bot):
    self.bot = bot 
    self.tts = aiogTTS()

  async def to_bytes(self, url):
    async with bot.session.get(url) as r:
      res = await r.read() 
      return res

  def to_text_(self, file):
    with sr.AudioFile(file) as source:
      audio = r.record(source)
    try:
      text = r.recognize_google(audio)
      return text
    except:
      return "<:redTick:596576672149667840> | I didn't get it."

  async def to_text(self, file):
    blocking = functools.partial(self.to_text_, file)
    res = await self.bot.loop.run_in_executor(None, blocking)
    return res

  @commands.command()
  async def speech(self, ctx):
    "Recognize a voice and make it text"
    async with ctx.typing():
      try:
        if ctx.message.attachments:

          if ctx.message.attachments[0].filename.endswith(".wav"):
            b = BytesIO()
            oof = await ctx.message.attachments[0].save(b)
            b.seek(0)
            text = await self.to_text(io.BytesIO(b.read()))
            emb = discord.Embed(description = text, colour = 0x36393E)
            return await ctx.send(embed = emb)

          else:
            return await ctx.send("Only `.wav` files.")
        else:
          return await ctx.send("Pls include an audio file")
      except Exception:
        traceback.print_exc()

  @commands.command(aliases = ["tts"])
  async def text_to_speech(self, ctx, *, message):
    "Transform a text to a speech!"

    temp = TemporaryFile()
    await self.tts.write_to_fp(fp = temp, text = message, lang = "en")
    temp.seek(0)
    f = discord.File(fp = io.BytesIO(temp.read()), filename = "tts.mp3")
    await ctx.send(ctx.author.mention, file = f)

def setup(bot):
  bot.add_cog(Speech(bot))