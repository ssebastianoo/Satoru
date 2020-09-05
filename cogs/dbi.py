import discord
from discord.ext import commands
import requests
from discord import Webhook, RequestsWebhookAdapter

class DBI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.guild.id == 611322575674671107

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def devban(self, ctx, member: discord.Member, *, reason = "Reason not given"):
        "Ban a member from ➥〙developing"
        channels = [self.bot.get_channel(612759413677096966), self.bot.get_channel(611333012210319372), self.bot.get_channel(657628300868583425)]

        for a in channels:
            await a.set_permissions(member, send_messages = False)

        ban_channels = "\n- ".join([a.mention for a in channels])
        emb = discord.Embed(description = f"**{member.mention} has been banned from the following channels:**\n\n- {ban_channels}\n\n>>> {reason}", colour = self.bot.colour)
        await ctx.send(embed = emb)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def devunban(self, ctx, *, member: discord.Member):
        "Unban a member from ➥〙developing"
        channels = [self.bot.get_channel(612759413677096966), self.bot.get_channel(611333012210319372), self.bot.get_channel(657628300868583425)]

        for a in channels:
            await a.set_permissions(member, send_messages = None)

        ban_channels = "\n- ".join([a.mention for a in channels])
        emb = discord.Embed(description = f"**{member.mention} has been unbanned from the following channels:**\n\n- {ban_channels}", colour = self.bot.colour)
        await ctx.send(embed = emb)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 741056705357414477:
            await message.add_reaction("<a:check:726040431539912744>")
            await message.add_reaction("<a:fail:727212831782731796>")

        elif message.channel.id == 743117154932621452:

            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url('url-here', adapter=AsyncWebhookAdapter(session))
                await webhook.send('Hello World', username='Foo')

            try: 
                actual = int(message.content)
            except ValueError:
                return await message.delete()
        
            msgs = await message.channel.history(limit = 2).flatten() 
            try:
                num = int(msgs[1].content)
            except:
                if actual == 1:
                    return  
                else: 
                    return await message.delete() 

            if msgs[1].author.id == message.author.id:
                return await message.delete()
            
            if actual == num + 1:
                if actual in [100, 500, 1000, 1500, 5000, 10000]:
                    await message.add_reaction("🎉")
                return   

            else:
                await message.delete()

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if channel.id == 743117154932621452:
            if message.id == channel.last_message.id:
                await message.delete()

def setup(bot):
    bot.add_cog(DBI(bot))