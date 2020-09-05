from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import aiohttp
import traceback

class Images(commands.Cog):

  def __init__(self, bot):
    self.bot = bot 

  async def has_transparency(self, img):
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True

    elif img.mode == "RGBA":
      extrema = img.getextrema()
      if extrema[3][0] < 255:
          return True

    return False

  async def mike(self, img):
    img = Image.open(BytesIO(img)).resize((500, 500))
    img.putalpha(100)
    base = Image.open('assets/mike.png').resize((500, 500))
    base.paste(img, (0, 0), img)
    b = BytesIO()
    base.save(b, "png")
    b.seek(0)
    return b

  async def punch(self, img1, img2):
    base = Image.open('assets/punch.png').convert("RGBA")
    
    mask1 = Image.open('assets/circle-mask.jpg').convert("L").resize((210, 210))
    mask2 = Image.open('assets/circle-mask.jpg').convert("L").resize((300, 300))

    img1 = Image.open(BytesIO(img1)).resize((210, 210)).convert("RGBA")
    img2 = Image.open(BytesIO(img2)).resize((300, 300)).convert("RGBA")

    if await self.has_transparency(img1):
      base.paste(img1, (40, 35), img1)
    else:
      base.paste(img1, (40, 35), mask1)
    if await self.has_transparency(img2):
      base.paste(img2, (480, 30), img2)
    else:
      base.paste(img2, (480, 30), mask2)
    b = BytesIO() 
    base.save(b, "png")
    b.seek(0)
    return b

  async def disabled(self, img):
    base = Image.open("assets/am-i-disabled.png").convert("RGBA").resize((1200, 900))
    img = Image.open(BytesIO(img)).resize((604, 604)).convert("RGBA").resize((604, 604))
    mask = Image.open("assets/homer-mask.jpg").convert("L").resize((604, 604))

    base.paste(img, (290, -25), mask)

    b = BytesIO() 
    base.save(b, "png")
    b.seek(0)

    return b

  @commands.command(aliases = ["cmm", "mind", "change me"])
  async def change_my_mind(self, ctx, *, text):

    "Change my mind meme"

    async with ctx.typing():

      async with aiohttp.ClientSession() as cs:
          async with cs.get(str(ctx.author.avatar_url_as(format = "png"))) as r:
              res = await r.read()  
        
      await cs.close()
      
      base = Image.open('assets/mind.png')
      img = Image.open(BytesIO(res)).resize((100, 100)).convert('RGBA').rotate(30)
      f = ImageFont.truetype('assets/Arial.ttf', 50)
      base.paste(img, (255, 6), img)

      # ---
      # d = ImageDraw.Draw(base)
      # d.text((400,300), str(text), fill=(0,0,0), font = f)
      # ---

      try:

        txt=Image.new('L', (500,500))
        d = ImageDraw.Draw(txt)
        d.text((0, 0), text,  font=f, fill = 255)
        w=txt.rotate(20,  expand=1)

        base.paste(ImageOps.colorize(w, (0,0,0), (0,0,0)), (380,100),  w)

      except Exception:
        traceback.print_exc()

      base = base.convert('RGBA')
      b = BytesIO() 
      base.save(b, "png") 
      b.seek(0)
      await ctx.send(file = discord.File(fp=b, filename = f"Change {ctx.author.display_name}'s mind.png"))

  @commands.command(name = "punch")
  async def _punch(self, ctx, *, member: discord.Member = None):

    "Punch someone"

    if not member:
      member = ctx.author

    if member == self.bot.user:
      return await ctx.send("no u")

    async with ctx.typing():

      async with aiohttp.ClientSession() as cs1:
          async with cs1.get(str(ctx.author.avatar_url_as(format = "png"))) as r:
              res2 = await r.read()  

      async with aiohttp.ClientSession() as cs2:
          async with cs2.get(str(member.avatar_url_as(format = "png"))) as r:
              res1 = await r.read()  

      b = await self.punch(res1, res2)

      await ctx.send(file = discord.File(fp=b, filename = "punch.png"))

      await cs1.close()
      await cs2.close()

  @commands.command(name = "mike")
  async def _mike(self, ctx, member: discord.Member = None):

    "Mike Bruhzowski"

    member = member or ctx.author

    async with ctx.typing():

      if ctx.message.attachments:
        url = ctx.message.attachments[0].url
      
      else:
        url = str(member.avatar_url_as(format = "png"))

      async with aiohttp.ClientSession() as cs:
          async with cs.get(url) as r:
              res = await r.read()  
              
      await cs.close()

      b = await self.mike(res)
      await ctx.send(file = discord.File(fp = b, filename = "mike.png"))


  @commands.command(name = "disabled")
  @commands.cooldown(1, 5, BucketType.user)
  async def _disabled(self, ctx, *, member: discord.Member = None):

    "Is someone disabled?"

    member = member or ctx.author

    if member == self.bot.user:
      return await ctx.send("no u")

    async with ctx.typing():

      if ctx.message.attachments:
        url = ctx.message.attachments[0].url
      
      else:
        url = str(member.avatar_url_as(format = "png"))

      async with aiohttp.ClientSession() as cs:
          async with cs.get(url) as r:
              res = await r.read()  

      await cs.close()

      b = await self.disabled(res)
      
      await ctx.send(file = discord.File(fp=b, filename = "disabled.png"))
    
  @commands.command()
  async def triggered(self, ctx, *, member: discord.Member = None):
    "Trigger a member"

    async with ctx.typing():

      member = member or ctx.author

      if ctx.message.attachments:
        if ctx.message.attachments[0].filename.endswith(("jpeg", "jpg", "webp", "png")):
          url = ctx.message.attachments[0].url
        else:
          url = str(member.avatar_url_as(format = "png"))
      
      else:
        url = str(member.avatar_url_as(format = "png"))

      url = "https://some-random-api.ml/canvas/triggered?avatar=" + url
      
      async with aiohttp.ClientSession() as cs:
        r = await cs.get(url)
        b = await r.read()

      await cs.close()

      await ctx.send("Powered by <https://some-random-api.ml/>", file = discord.File(fp = BytesIO(b), filename = f"{member.display_name}.gif")) 

def setup(bot):
  bot.add_cog(Images(bot))