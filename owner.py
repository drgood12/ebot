import discord, asyncio, os, random, time
from .utils import checks
from discord.ext import commands
from random import randint
from .utils import pagify

class Owner:

    def __init__(self, bot):
        self.bot = bot
        self.owners = ['421698654189912064', '269340844438454272']
        self.locked = 'This command is locked to: `Developer`'

    async def _confirm_invite(self, server, owner, ctx):
        answers = ("yes", "y")
        invite_dest = \
            self.get_default_channel_or_other(server, None,
                                              create_instant_invite=True, max_age=86400)
        if invite_dest is None:
            return await self.bot.say("Could not generate invite.")
        invite = await self.bot.create_invite(invite_dest, max_age=86400)
        if ctx.message.channel.is_private:
            await self.bot.say(invite)
        else:
            await self.bot.say("Are you sure you want to post an invite to {} "
                               "here? (yes/no)".format(server.name))
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is None:
                await self.bot.say("I guess not.")
            elif msg.content.lower().strip() in answers:
                await self.bot.say(invite)
            else:
                await self.bot.say("Alright then.")




    @commands.command(pass_context=True)
    @checks.is_owner()
    async def msg(self, ctx, channel: int, *, message: str):
        """ Message a channel in a server """
        to = discord.Object(id=channel)
        embed = discord.Embed(title="Message from my developer:", description=message, color=0xff2b2b)
        embed.set_footer(text=" •   Message from {}".format(ctx.message.author.name),
                         icon_url=ctx.message.author.avatar_url)
        if ctx.message.author.id in self.owners:
            try:
                await self.bot.send_message(to, embed=embed)
                await self.bot.say("Success.")
            except Exception as e:
                await asyncio.sleep(2)
                await self.bot.say(
                    "failed to send embed/message: ```py\n{}\n```\nattempting to send regular msg...".format(e))
                await asyncio.sleep(2)
                try:
                    await self.bot.send_message(to, message)
                    await self.bot.say("Sent as regular text.")
                except Exception as e:
                    await self.bot.say("Another error occured: ```py\n{}\n```".format(e))
        else:
            await self.bot.say(self.locked)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def serverslist(self, ctx):
        """Servers"""
        if ctx.message.author.id in self.owners:
            for server in self.bot.servers:
                msg = f"```py\n{server.name} : {server.id}\n```"
                await self.bot.say(msg)
                await asyncio.sleep(1)

    # guess

    @commands.command(hidden=True)
    @checks.is_owner()
    async def cogs(self):
        dir = os.listdir("cogs")
        embed = discord.Embed(title="Cogs in `cogs.`:", description="```diff\n+ {}\n```".format(dir), color=0xfac905)
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def leave(self, ctx):
        try:
            await self.bot.delete_message(ctx.message)
        except discord.Forbidden:
            pass
        finally:
            await self.bot.leave_server(ctx.message.server)

    @commands.command(pass_context=True, name='saylol')
    @checks.is_owner()
    async def boot(self, ctx, ting: str = False, *, msg: str):
        if ctx.message.author.id in self.owners:
            ting = ting
            aa = ['true', 'True', 't', 'T']
            da = ['False', 'false', 'f', 'F']
            if ting == discord.Member:
                title = "message from {}:".format(ting)
            elif ting not in aa:
                title = "Message from **UNKNOWN**:"
            else:
                title = "Message from Ebot 2.0:"

            try:
                await self.bot.delete_message(ctx.message)
                embed = discord.Embed(title=title.format(ctx.message.author), description=msg, color=0xfac905)
                await self.bot.say(embed=embed)
            except Exception as e:
                try:
                    embed = discord.Embed(title=title.format(ctx.message.author), description=msg, color=0xfac905)
                    embed.set_footer(text=f"❌ An error occured while preforming this command:\n {e}")
                    await self.bot.say(embed=embed)
                except Exception as error:
                    await self.bot.whisper(
                        f"❌ i might not have `embed links` permission, or `send messages`. in case it isnt that, this is your error: `{error}`."
                        "\nTry running -perms <@517008210905923594> to see if i have them.")
        else:
            await self.bot.say(locked)

    async def _confirm_invite(self, server, owner, ctx):
        answers = ("yes", "y")
        invite_dest = \
            self.get_default_channel_or_other(server, None,
                                              create_instant_invite=True)
        if invite_dest is None:
            return await self.bot.say("Could not generate invite.")
        invite = await self.bot.create_invite(invite_dest, max_age=86400)
        if ctx.message.channel.is_private:
            await self.bot.say(invite)
        else:
            await self.bot.say("Are you sure you want to post an invite to `{}` "
                               "here? (yes/no)".format(server.name))
            msg = await self.bot.wait_for_message(author=owner, timeout=15)
            if msg is None:
                await self.bot.say("I guess not.")
            elif msg.content.lower().strip() in answers:
                await self.bot.say(invite)
            else:
                await self.bot.say("Alright then.")

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def inv(self, ctx, idnum=None):
        """Lists servers and generates invites for them"""
        owner = ctx.message.author
        if ctx.message.author.id in self.owners:
            owner = ctx.message.author
            if idnum:
                server = discord.utils.get(self.bot.servers, id=idnum)
                if server:
                    await self._confirm_invite(server, owner, ctx)
                else:
                    await self.bot.say("I'm not in that server")
        else:
            await self.bot.say(self.locked)

    @commands.command(pass_context=True, hidden=True)
    @checks.is_owner()
    async def repeat(self, ctx, times: int = 100, *, msg: str):
        """repeats x times"""
        if ctx.message.author.id in self.owners:
            for i in range(times):
                await self.bot.say(msg)
                await asyncio.sleep(0.5)
        else:
            await self.bot.say(self.locked)  # suggest

    def get_default_channel_or_other(self, server,
                                     ctype: discord.ChannelType = None,
                                     **perms_required):

        perms = discord.Permissions.none()
        perms.update(**perms_required)
        if ctype is None:
            types = [discord.ChannelType.text, discord.ChannelType.voice]
        elif ctype == discord.ChannelType.text:
            types = [discord.ChannelType.text]
        else:
            types = [discord.ChannelType.voice]
        try:
            channel = server.default_channel
        except Exception:
            channel = None
        if channel is not None:
            if channel.permissions_for(server.me).is_superset(perms):
                return channel

        chan_list = [c for c in sorted(server.channels,
                                       key=lambda ch: ch.position)
                     if c.type in types]
        for ch in chan_list:
            if ch.permissions_for(server.me).is_superset(perms):
                return ch

        return None

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def servers(self, ctx, it: int):
        """Lists and allows to leave servers"""
        owner = ctx.message.author

        msg = await self.bot.wait_for_message(author=owner, timeout=15)
        try:
            msg = int(msg.content)
            await self.leave_confirmation(it, owner, ctx)

        except (IndexError, ValueError, AttributeError):
            pass

    async def leave_confirmation(self, server, owner, ctx):
        await self.bot.say("Are you sure you want me "
                           "to leave {}? (yes/no)".format(server.name))

        msg = await self.bot.wait_for_message(author=owner, timeout=15)

        if msg is None:
            await self.bot.say("I guess not.")
        elif msg.content.lower().strip() in ("yes", "y"):
            await self.bot.leave_server(server)
            if server != ctx.message.server:
                await self.bot.say("Done.")
        else:
            await self.bot.say("Alright then.")


    @commands.command()
    @checks.is_owner()
    async def bancheck(self):
        """Sweeps through and leaves banned servers"""
        counter = 0
        banned = ['504050383338078229']
        for server in list(self.bot.servers):
            if server.id in banned:
                await self.bot.leave_server(server)
                await self.bot.say(f"left {server}")
                counter +=1
            else:
                pass


        if counter != 0:
            await self.bot.say("Left {} servers".format(counter))
        else:
            await self.bot.say("Not in any banned servers.")

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def upload(self, ctx, file: str):
        """Upload a file"""
        start = time.time()
        try:
            await self.bot.send_typing(ctx.message.channel)
            await self.bot.send_file(ctx.message.channel, file)
            end = time.time()
            result = round(end - start)
            await self.bot.say("Success! {}s".format(result))
        except FileNotFoundError:
            await self.bot.say("Error: File not found. did you do the right dir? (defaults to `core.py`'s folder)")



def setup(bot):
    bot.add_cog(Owner(bot))