import discord, random, json
from discord.ext import commands 

class HelpCommand:
    def __init__(self, bot):
        self.bot = bot

    def get_type(self, command):
        "check if a command or a cog is passed"

        if self.bot.get_command(command):
            return "command"
        
        elif self.bot.get_cog(command):
            return "cog"

        else:
            return None
        
    async def command_not_found(self, ctx, command):
        "command not found error"
        emb = discord.Embed(description = f"```\ncommand \"{command}\" not found!\n```", colour = discord.Colour.red())
        return await ctx.send(embed = emb)

    async def cog_not_found(self, ctx, cog):
        "command not found error"
        emb = discord.Embed(description = f"```\ncog \"{cog}\" not found!\n```", colour = discord.Colour.red())
        return await ctx.send(embed = emb)

    async def command_list(self, ctx):
        "return the commands list"

        with open("data/prefixes.json", "r") as f:
            l = json.load(f)

        try:
            prefix = l[str(ctx.guild.id)]

        except KeyError:
            prefix = "e?"

        self.description = f"""Server Prefixes: `{prefix}`, `@{self.bot.user}`
[Support Server](https://discord.gg/w8cbssP)"""

        emb = discord.Embed(title = "Help", description = f"{self.description}\n\n", colour = self.bot.colour, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = str(ctx.author.avatar_url_as(static_format = "png")))
        
        for cog in self.bot.cogs:
            cog = self.bot.get_cog(cog)
            cog_str = f"**{cog.qualified_name.upper()}\n**"
            commands = cog.get_commands()
            commands = [cmd for cmd in commands if not cmd.hidden]

            if len(commands) >= 1:
                for command in commands:
                    cog_str += f"`{command.name}` " 

                    try:
                        for cmd in command.commands:
                            cog_str += f"`{cmd.parent} {cmd.name}` " 
                    except:
                        pass

                emb.description += f"{cog_str}\n\n"
        
        return await ctx.send(embed = emb)

    async def command(self, ctx, command: commands.Command):
        "return single command help"

        if command.hidden:
            return await self.command_not_found(ctx, command.name)

        emb = discord.Embed(title = "Help", description = command.help, colour = self.bot.colour, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = str(ctx.author.avatar_url_as(static_format = "png")))

        try:
            parent = command.parent  
        except:
            parent = None

        if parent:
            usage = f"```{command.parent} {command.name}{command.signature}```" if command.signature else f"```{command.parent} {command.name}```"
            emb.add_field(name = "Usage", value = usage)

            if command.aliases:
                aliases = "\n".join([f"{cmd}" for cmd in command.aliases])
                emb.add_field(name = "Aliases", value = '```\n{}\n```'.format(aliases))
            
            emb.add_field(name = "Parent", value = f"```\n{command.parent}\n```")

            return await ctx.send(embed = emb)

        else:
            usage = f"```{command.name} {command.signature}```" if command.signature else f"```{command.name}```"
            emb.add_field(name = "Usage", value = usage)

            if command.aliases:
                aliases = "\n".join([f"{cmd}" for cmd in command.aliases])
                emb.add_field(name = "Aliases", value = '```\n{}\n```'.format(aliases))

            try:
                if command.commands:
                    subcommands = ""
                    for cmd in [c for c in command.commands if not c.hidden]:
                        subcommands += f"{cmd.parent} {cmd.name} {cmd.signature}\n"
                        
                    emb.add_field(name = "Subcommands", value = f"```\n{subcommands}\n```")

            except:
                pass

            return await ctx.send(embed = emb)

    async def cog(self, ctx, cog: commands.Cog):
        "return cog commands"
        
        def __init__(self, description = None):
            self.description = description

        emb = discord.Embed(title = cog.qualified_name, description = "", colour = self.bot.colour, timestamp = ctx.message.created_at)
        emb.set_author(name = ctx.author, icon_url = str(ctx.author.avatar_url_as(static_format = "png")))
        
        commands = cog.get_commands()
        commands = [cmd for cmd in commands if not cmd.hidden]

        cog_str = f"**{cog.qualified_name.upper()}**\n"

        if len(commands) >= 1:
            for command in commands:
                cog_str += f"`{command.name} {command.signature}` " if command.signature else f"`{command.name}` " 

                try:
                    for cmd in command.commands:
                        cog_str += f"`{cmd.parent} {cmd.name} {cmd.signature}` " if command.signature else f"`{cmd.parent} {cmd.name}` " 
                except:
                    pass

            emb.description = cog_str

        else:
            return await self.cog_not_found(ctx, cog.qualified_name)

        return await ctx.send(embed = emb)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        self.help = HelpCommand(bot)
        bot.help_command = None

    @commands.command(hidden = True)
    async def help(self, ctx, command = None):
        "stop it, get some help"

        if not command:
            await self.help.command_list(ctx)
        
        else:
            if self.help.get_type(command) == "command":
                await self.help.command(ctx, self.bot.get_command(command))

            elif self.help.get_type(command) == "cog":
                await self.help.cog(ctx, self.bot.get_cog(command))

            else:
                await self.help.command_not_found(ctx, command)

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Help(bot))