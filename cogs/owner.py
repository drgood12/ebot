import discord, asyncio, os, random, time, collections, requests
from .utils import checks
from .utils.pagify import pagify, box
from discord.ext import commands
from random import randint


class Owner:

    def __init__(self, bot):
        self.bot = bot
        self.owners = ['421698654189912064', '269340844438454272', '493790026115579905']
        self.locked = 'This command is locked to: `Developer`'
        self.donators = ['421698654189912064', '415912795574501386', '344878404991975427', '269340844438454272',
                         '293066151695482882', '493790026115579905', '365659613821009920']

    async def _confirm_invite(self, server, owner, ctx):
        answers = ("yes", "y")
        invite_dest = \
            self.get_default_channel_or_other(server, None,
                                              create_instant_invite=True, max_age=86400)
        if invite_dest is None:
            return await self.bot.say("Could not generate invite.")
        invite = await self.bot.create_invite(invite_dest, max_age=86400, max_uses=2)
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
    async def serverlist(self, ctx):
        """Servers"""
        msg = "```py\n"
        if ctx.message.author.id in self.owners:
            for server in self.bot.servers:
                msg += f"{server.name} : {server.id}\n"
            msg += "```"
            await self.bot.say(msg)

    # guess

    @commands.command(hidden=True)
    @checks.is_owner()
    async def cogs(self):
        dir = os.listdir("cogs")
        embed = discord.Embed(title="Files in `cogs.`:", description="```diff\n+ {}\n```".format(dir), color=0xfac905)
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
            await self.bot.say(self.locked)

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


    @commands.command()
    @checks.is_owner()
    async def bancheck(self):
        """Sweeps through and leaves banned servers"""
        counter = 0
        banned = ['504050383338078229', '526438179574906881', '504539562861789204']
        for server in list(self.bot.servers):
            if server.id in banned:
                await self.bot.leave_server(server)
                await self.bot.say(f"left {server}")
                counter += 1
            else:
                pass

        if counter != 0:
            await self.bot.say("Left {} servers".format(counter))
        else:
            await self.bot.say("Not in any banned servers.")

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def upload(self, ctx, file: str):
        """Upload a file"""
        if ctx.invoked_subcommand is None:
            start = time.time()
            await self.bot.delete_message(ctx.message)
            try:
                await self.bot.send_typing(ctx.message.channel)
                h = await self.bot.send_file(ctx.message.channel, file)
                end = time.time()
                result = round(end - start)
                h2 = await self.bot.say("Success! {}s".format(result))
                if file == 'core.py':
                    await self.bot.edit_message(h, "Self-destruct in 20s")
                    await asyncio.sleep(10)
                    await self.bot.edit_message(h, "Self-destruct in 10s")
                    await asyncio.sleep(7)
                    await self.bot.edit_message(h, "\*Explosion in the distance*")
                    await asyncio.sleep(3)
                    await self.bot.delete_message(h)
                    await self.bot.delete_message(h2)
            except FileNotFoundError:
                await self.bot.say("Error: File not found. did you do the right dir? (defaults to `core.py`'s folder)")
        else:
            return

    @commands.command()
    @checks.is_owner()
    async def pc(self, chars: int = 2019):
        """Check if pagify feckin works"""
        msg = ""
        pages = 1
        charsc = 0
        for i in range(chars):
            msg += "a"
            charsc += 1
        for page in pagify(msg):
            await self.bot.say(page)
            pages += 1
        await self.bot.say(f"Sent {int(pages) - 1} pages ({charsc} numbers)")

    @commands.command()
    @checks.is_owner()
    async def useless(self):
        """Idk line-filler i guess"""
        strt = time.monotonic()
        counter = 0
        for server in self.bot.servers:
            counter += 1
            for channel in server.channels:
                counter += 1
            for members in server.members:
                counter += 1
            for role in server.roles:
                counter += 1
        msg = await self.bot.say(counter)
        end = round(time.monotonic() - strt)
        await self.bot.edit_message(msg, end)

    @commands.command(pass_context=True)
    @checks.is_owner()
    async def reboot(self, ctx, shutdown_mode: str = 'true', silent: str = 'false'):
        """reboot"""
        try:
            await self.bot.add_reaction(ctx.message, 'lol:547895677653614630')
            await self.bot.clear_reactions(ctx.message)
            await self.bot.add_reaction(ctx.message, '🇰')
            await self.bot.clear_reactions(ctx.message)
            await self.bot.add_reaction(ctx.message, '🇧')
            await self.bot.add_reaction(ctx.message, '🇦')
            await self.bot.add_reaction(ctx.message, '🇮')
        except:
            pass
        try:
            if silent == 'false':
                await self.bot.change_presence(game=discord.Game(name="Rebooting..."), status=discord.Status.dnd)
                await asyncio.sleep(5)
            else:
                pass
            await self.bot.close()
        except discord.HTTPException:
            pass
        finally:
            if shutdown_mode == 'false':
                exit()
            else:
                os.system("python3 core.py")

    @commands.command()
    async def post(self):
        """Post stats to discordbotlist.com"""
        token = 'ye no'
        a = await self.bot.say("Getting stats <a:loading:551413963766890527>")
        payload = {
            'shard_id': '0',
            'guilds': len(self.bot.servers),
            'users': len(set(self.bot.get_all_members())),
            'voice_connections': 0}  # idk how to fill that in lol
        headers = {'Authorization': f'Bot {token}'}
        url = f'https://discordbotlist.com/api/bots/{self.bot.user.id}/stats'
        await self.bot.edit_message(a, "Posting <a:loading:551413963766890527>")
        r = requests.post(url, headers=headers, data=payload)
        if r.status_code == 204:
            await self.bot.edit_message(a, f'Successfully posted stats to {url} <:success:522078924432343040>')
        else:
            await self.bot.edit_message(a, f'Status code: {r.status_code} <:fail:522076877075251201>')








def setup(bot):
    bot.add_cog(Owner(bot))