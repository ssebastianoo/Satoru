import discord, requests, aiohttp, asyncio, random
from discord.ext import commands

class DBI(commands.Cog, command_attrs = dict(hidden = True)):

    def __init__(self, bot):
        self.bot = bot
        self.bot.invite_converter = commands.InviteConverter()

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

        elif message.channel.id == 762752717281558568:
            if message.author == self.bot.user:
                return

            if len(message.content.split(" ")) >= 2:
                return

            else:
                ctx = commands.Context(prefix = "no", bot = self.bot, message = message)
                try:
                    invite = await self.bot.invite_converter.convert(ctx, message.content)

                except:
                    await message.channel.send("not a valid server invite link", delete_after = 5)
                    await asyncio.sleep(5)
                    return await message.delete()
                
                await message.delete()
                await ctx.send(f"**{message.author}** https://discord.gg/{invite.code}")

        elif message.channel.id == 743117154932621452:

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

        elif message.channel.id == 611325092269522944:
            if message.attachments:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

            elif message.embeds:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

        else:
            emoji = "🎄"
            choice = random.choice(range(0, 25))
            if choice == 5:
                await message.add_reaction(emoji)
            else:
                return

            def check(reaction, user):
                return str(reaction.emoji) == emoji and reaction.message.id == message.id

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=500)

            except asyncio.TimeoutError:
                return await message.remove_reaction(emoji, message.guild.me)

            winner = user.id
            data = await self.bot.cursor.execute("SELECT * FROM trees where user = ?", (winner,))
            data = await data.fetchall()

            if len(data) == 0:
                await self.bot.cursor.execute("INSERT into trees (user, trees) VALUES (?, ?)", (winner, 1))

            else:
                trees = int(data[0][1]) + 1
                await self.bot.cursor.execute("UPDATE trees set trees = ? where user = ?", (trees, winner))

    def is_dbi(self):
        async def predicate(self, ctx):
            return ctx.guild.id == 611322575674671107
        return commands.check(predicate)
    
    @commands.command(aliases=["alberi", "tree", "points", "punti"])
    @self.is_dbi()
    async def trees(self, ctx, *, member: discord.Member = None):
        "Quanti alberi hai?"

        member = member or ctx.author

        async with ctx.typing():
            data = await self.bot.cursor.execute("SELECT * FROM trees where user = ?", (member.id,))
            data = await data.fetchall()

            if len(data) == 0:
                word = "Albero"
                trees = 1
            else:
                word = "Alberi"
                trees = int(data[0][1])

            emb = discord.Embed(description = f"**{trees} {word}** 🎄", colour = self.bot.colour).set_author(name=member.display_name, icon_url=str(member.avatar_url_as(static_format="png")))
            await ctx.send(embed = emb)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if channel.id == 743117154932621452:
            if message.id == channel.last_message.id:
                await message.delete()

        elif message.channel.id == 611325092269522944:
            if message.attachments:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

            elif message.embeds:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.channel.id == 611325092269522944:
            ups = discord.utils.get(message.reactions, emoji = "👍")
            downs = discord.utils.get(message.reactions, emoji = "👎")

            if ups.count >= downs.count:
                return

            elif downs.count > ups.count and downs.count > 4:
                await message.delete()

def setup(bot):
    bot.add_cog(DBI(bot))
