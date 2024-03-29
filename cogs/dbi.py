import discord, requests, aiohttp, asyncio, random
from discord.ext import commands
from ext.checks import *

class DBI(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot
        self.bot.invite_converter = commands.InviteConverter()

    async def cog_check(self, ctx):
        return ctx.guild.id == 611322575674671107

    @commands.command()
    @is_dbi()
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
    @is_dbi()
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

        elif message.channel.id == config.dbi.counting:

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

        elif message.channel.id == config.dbi.memes:
            if message.attachments:
                await message.add_reaction("👍")
                await asyncio.sleep(0.2)
                await message.add_reaction("👎")

            elif message.embeds:
                await message.add_reaction("👍")
                await asyncio.sleep(0.2)
                await message.add_reaction("👎")

        elif message.channel.id == config.dbi.circo:
            await message.publish()

    @commands.command(aliases=["cup", "trofei", "points", "punti"])
    @is_dbi()
    async def cups(self, ctx, *, member: discord.Member = None):
        "Quante coppe clown hai?"

        member = member or ctx.author

        async with ctx.typing():
            data = await self.bot.db.execute("SELECT * FROM trees where user = ?", (member.id,))
            data = await data.fetchall()

            if len(data) == 0:
                trees = 0
            else:
                trees = int(data[0][1])

            if trees == 1:
                word = "Clown Cup"
            else:
                word = "Clown Cups"

            emb = discord.Embed(description = f"**{trees} {word}** {str(self.bot.get_emoji(config.dbi.clown_cup))}", colour = self.bot.colour).set_author(name=member.display_name, icon_url=str(member.avatar_url_as(static_format="png")))
            await ctx.send(embed = emb)

    @commands.command(aliases=["lb"])
    @is_dbi()
    async def leaderboard(self, ctx):
        "Chi ha più coppe clown?"

        async with ctx.typing():
            data = await self.bot.db.execute("SELECT * FROM trees")
            data = await data.fetchall()

            stats_ = {}

            for element in data:
                stats_[int(element[0])] = int(element[1])

            stats = sorted(stats_, key=lambda x: stats_[x], reverse=True)
            emb = discord.Embed(title="Leaderboard", description = "", colour = self.bot.colour)

            count = 1
            for user_id in stats:
                if count > 10:
                    break
                try:
                    user = await self.bot.fetch_user(user_id)
                except Exception as e:
                    print(e)
                    user = None

                if user:
                    emb.description += f"`{count}.` **{str(user)}** `{stats_[user.id]}`{str(self.bot.get_emoji(config.dbi.clown_cup))}\n"
                    count += 1
            await ctx.send(embed = emb)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        channel = self.bot.get_channel(payload.channel_id)

        try:
            message = await channel.fetch_message(payload.message_id)
        except:
            return

        if channel.id == config.dbi.counting:
            if message.id == channel.last_message.id:
                await message.delete()

        elif message.channel.id == config.dbi.memes:
            if message.attachments:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

            elif message.embeds:
                await message.add_reaction("👍")
                await message.add_reaction("👎")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.guild_id != config.dbi.id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.channel.id == config.dbi.memes:
            ups = discord.utils.get(message.reactions, emoji = "👍")
            downs = discord.utils.get(message.reactions, emoji = "👎")

            if downs.count > ups.count and downs.count > 4:
                await message.delete()

        if payload.emoji.id == config.dbi.clown_cup:
            data = await (await self.bot.db.execute("SELECT message FROM treesmessages WHERE message=?", (message.id,))).fetchone()
            if data:
                await self.bot.db.execute("DELETE FROM treesmessages WHERE message=?", (message.id,))
                data = await self.bot.db.execute("SELECT * FROM trees WHERE user=?", (payload.member.id,))
                data = await data.fetchone()

                if not data:
                    await self.bot.db.execute("INSERT INTO trees (user, trees) VALUES (?, ?)", (payload.member.id, 1))

                else:
                    trees = int(data[0][1]) + 1
                    await self.bot.db.execute("UPDATE trees set trees=? where user=?", (trees, payload.member.id))

                await self.bot.db.commit()
                await message.clear_reaction(emoji)

def setup(bot):
    bot.add_cog(DBI(bot))
