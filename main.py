
import random
from random import randint
import asyncio
import logging
import time
import discord
import os
import collections
from .utils import checks
from discord.ext import commands


##################################################
#print ("Current Year is: %d" % currentDT.year)
#print ("Current Month is: %d" % currentDT.month)
#print ("Current Day is: %d" % currentDT.day)
#print ("Current Hour is: %d" % currentDT.hour)
#print ("Current Minute is: %d" % currentDT.minute)
#print ("Current Second is: %d" % currentDT.second)
#print ("Current Microsecond is: %d" % currentDT.microsecond)



def is_owner(ctx):
    return ctx.message.author.id in ["421698654189912064", "269340844438454272"]

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='test2.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

start_time = time.time()

#stats ping
class CoreCommands:

    def __init__(self, bot):
        self.bot = bot
        self.bpt = bot
        self.owners = ['421698654189912064', '269340844438454272']
        self.locked = 'This command is locked to: `Developer`.'
        self.donators = ['421698654189912064', '415912795574501386', '344878404991975427', '269340844438454272']


    @commands.command(name='help', pass_context=True)
    async def _help(self, ctx, command = None):
        """Embedded help command"""
        author = ctx.message.author
        
        if not command:
            msg = "**Command list:**"
            color = randint(0, 0xffffff)


            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if self.bot.commands[com].module.__name__ not in com_groups:
                        com_groups.append(self.bot.commands[com].module.__name__)
                    else:
                        continue
                except Exception as e:
                        print(e)
                        continue
            com_groups.sort()
            alias = []
            #print(com_groups)
            for com_group in com_groups:
                commands = []
                for com in self.bot.commands:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    if com in self.bot.commands[com].aliases:
                        continue
                    if com_group == self.bot.commands[com].module.__name__:
                        commands.append(com)
                final_coms[com_group] = commands

            to_send = []

            final_coms = collections.OrderedDict(sorted(final_coms.items()))
            field_count = 0
            page = 0
            counter = 0

            for group in final_coms:
                counter += 1
                if field_count == 0:
                    page += 1
                    title = "**Command list,** page {}".format(page)
                    em=discord.Embed(description=title,
                                     color=color)
                    em.set_thumbnail(url="https://cdn.discordapp.com/avatars/517008210905923594/7a769765fda1fa7e9469d4bf6f3dbbf2.webp?size=1024")

                field_count += 1
                is_last = counter == len(final_coms)
                msg = ""
                final_coms[group].sort()
                count = 0
                for com in final_coms[group]:
                    if count == 0:
                        msg += '{}'.format(com)
                    else:
                        msg += ', {}'.format(com)
                    count += 1

                cog_name = group.replace("cogs.", "").title()
                cog =  "```\n"
                cog += cog_name
                cog += "\n```"
                em.add_field(name=cog,
                             value=msg,
                             inline=False)

                if field_count == 15 or is_last:
                    to_send.append(em)
                    field_count = 0


        
            await self.bot.say(embed=em)
                
        else:
            msg = "**Command Help:**"
            color = 0xffa500

            em=discord.Embed(description=msg,
                             color=color)
            try:
                if not self.bot.commands[command].can_run(ctx):
                    await self.bot.say("Might be lacking perms for this "
                                       "command.")
                    return
                commie =  "```\n"
                commie += command + " " + " ".join(["[" + com + "]" for com in \
                                                    self.bot.commands[command].\
                                                    clean_params])
                commie += "\n```"
                info = self.bot.commands[command].help
                em.add_field(name=commie,
                             value=info,
                             inline=False)
                await self.bot.say(embed=em)
            except Exception as e:
                print(e)
                await self.bot.say("Couldn't find command! Try again.")


    async def on_server_join(self,server):
        jembed=discord.Embed(title="I joined {}!".format(server), description="Now in {} servers (on this shard)!".format(len(self.bot.servers)), color=randint(0,0xffffff))
        jembed.add_field(name="Members", value=server.member_count)
        jembed.add_field(name="owner",value=server.owner)
        jembed.add_field(name="region", value=server.region)
        jembed.set_footer(text=server.id)
        jembed.set_thumbnail(url="{}".format(server.icon_url))
        banned = ['504050383338078229']
        banned = ['504050383338078229']
        for server in list(self.bot.servers):
            if server.id in banned:
                await self.bot.leave_server(server)
                print(f"left {server}")
        await self.bot.send_message(discord.Object(id=543496620743065620), embed=jembed)
        await self.bot.change_presence(game=discord.Game(name=f"{len(self.bot.servers)} servers! | Prefix: - or >"), status=None)


    async def on_server_remove(self, server):
        jembed=discord.Embed(title="I left {}!".format(server), description="Now in {} servers on this shard.".format(len(self.bot.servers)),color=randint(0, 0xffffff))
        jembed.add_field(name="Members", value=server.member_count)
        jembed.add_field(name="owner",value=server.owner)
        jembed.add_field(name="region", value=server.region)
        jembed.set_footer(text=server.id)
        jembed.set_thumbnail(url="{}".format(server.icon_url))
        await self.bot.send_message(discord.Object(id=543496620743065620), embed=jembed)
        await self.bot.change_presence(game=discord.Game(name=f"{len(self.bot.servers)} servers! | Prefix: - or >"),
                                       status=None)



        msg="""
import discord, random
from random import randint
jembed=discord.Embed(title="I joined {}!".format(server), description="Now in {} servers (on this shard)!".format(len(bot.servers)), color=randint(0, 0xffffff))
jembed.add_field(name="Members", value=server.member_count)
jembed.add_field(name="owner",value=server.owner)
jembed.add_field(name="region", value=server.region)
jembed.set_footer(text=server.id)
jembed.set_thumbnail(url="{}".format(server.icon_url))
await bot.send_message(discord.Object(id=543496620743065620), embed=jembed)
        """



    async def on_command_error(self, error, ctx):
        fmter = f"```py\n{error}\n```"
        lfmtr = f'```py\n{error.__class__.__name__}: {error}\n```'
        embed=discord.Embed(title=f"Error in {ctx.message.server.name}:", description=f"{ctx.message.server.id}",color=0xff2b2b)
        embed.add_field(name="Short error:",value=fmter)
        embed.add_field(name="Long error:", value="See below")
        embed.add_field(name="Executor:", value=f"{ctx.message.author}, {ctx.message.author.id}")
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):  #userinfo
            return
        else:
            await self.bot.send_message(discord.Object(id=542094899965591563), embed=embed)
            await self.bot.send_message(discord.Object(id=542094899965591563), lfmtr)
            if isinstance(error, discord.errors.InvalidArgument):
                await self.bot.send_message(ctx.message.channel, f"Argument error: ```py\n{error}\n```")
                return
            
            if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
                await self.bot.send_message(ctx.message.channel, "Missing arguments! Please use my help command to check them.")
                return
            if isinstance(error, commands.CommandOnCooldown):
                if error.retry_after >= 600:
                    x = (error.retry_after / 600) / 6
                    await self.bot.send_message(ctx.message.channel, 'This command is on a cooldown. try again in %.2fh' % x)
                    return
                else:
                    if error.retry_after >= 60:
                        x = error.retry_after / 60
                        await self.bot.send_message(ctx.message.channel, 'This command is on a cooldown. try again in %.2fm' % x)
                        return
                    else:
                        if error.retry_after <= 60:
                            await self.bot.send_message(ctx.message.channel, 'this command is on a cooldown. try again in %.2fs' & error.retry_after)
                            return
            if isinstance(error, discord.ext.commands.errors.CheckFailure):
                pass
            else:
                e = error
                e = discord.Embed(title="<:fail:522076877075251201> Unhandled Error:", description=f"```\n{error}\n```", color=0xff2b2b)
                e.add_field(name="How to fix:", value="Please report this [to my developer](https://invite.gg/Ebot) or [open an issue on github](https://github.com/EEKIM10/cogs/issues/new)")
                try:
                    await self.bot.send_message(ctx.message.channel, embed=e)
                except:
                    await self.bot.send_message(ctx.message.channel, f"```py\n{error}\n```")
                if ctx.message.author.id == '421698654189912064':
                    await self.bot.send_message(ctx.message.channel, "More info in terminal")
                    raise error
                if ctx.message.author.id == '269340844438454272':
                    await self.bot.send_message(ctx.message.channel, "The code has been sent to terminal. EEK will provide if you ping.")
                    raise error
                else:
                    await self.bot.send_message(ctx.message.channel,"please report this to my developer")  
                    raise error

              

    #ping       purge       userinfo    invite  serverinfo  news

    @commands.command(pass_context=True)
    async def quote(self, ctx, message_id: int, channel_id: int = None):
        """Get a quote from a message ID"""
        if channel_id == None:
            channel = ctx.message.channel
        elif channel_id != None or int:
            await self.bot.say("Error: channel_id takes `int`")
        else:
            channel = discord.Object(id=channel_id)

        try:
            msg = await self.bot.get_message(channel=channel, id=message_id)
            cntnt = msg.content
            await self.bot.say("{} says:\n```{}```".format(msg.author.name, cntnt))
        except (discord.NotFound, discord.HTTPException, discord.Forbidden) as e:
            await self.bot.say(f"```py\n{e}\n```")



    
    @commands.command()
    async def test(self):
        """testing xdlul"""
        await self.bot.say("<:success:522078924432343040>")

    @commands.command()
    async def raffle(self, debug: int = 0):
        """
        scratch card!
        Notice: does NOT affect anything. purely fun.
        """
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z']
        color1 = randint(0, 0xffffff)

        winornot = ['1', '0']
        #choice choosers 
        a = random.choice(letters)
        b = random.choice(letters)
        c = random.choice(letters)
        d = random.choice(letters)
        e = random.choice(letters)
        f = random.choice(letters)

        kk = random.choice(winornot)
        embed=discord.Embed(title="You bought a scratch card from thin air!", description=f"You got:\n||  {a}  || ||  {b}  || ||   {c}   || ||   {d}   || ||   {e}   || ||   {f}   ||", color=color1)
        kk = random.choice(winornot)
        if kk == '1':
            embed.add_field(name="Winning letters:", value=f"{a} {b} {c} {d} {e} {f}")
        else:
            A = random.choice(letters)
            B = random.choice(letters)
            C = random.choice(letters)
            D = random.choice(letters)
            E = random.choice(letters)
            F = random.choice(letters)
            embed.add_field(name="Winning letters:", value=f"{A} {B} {C} {D} {E} {F}")

        if debug == 0:
            pass
        if debug == 1:
            embed.set_footer(text="winornot = {}".format(kk))

        await self.bot.say(embed=embed)

    @commands.command()
    async def shardinfo(self):
        """Get sharded info"""
        e=discord.Embed(title="How it works:")  #purge 

    @commands.command(pass_context=True)
    async def compare(self, ctx, user: discord.User = None):
        """Compare channel access with [user]"""
        author = ctx.message.author
        if user is None:
            return
        
        
        server = ctx.message.server

        text_channels = [c for c in server.channels if str(c.type) == "text"]
        voice_channels = [c for c in server.channels if str(c.type) == "voice"]

        author_text_channels = [
            c.name for c in text_channels if c.permissions_for(author).read_messages is True
        ]
        author_voice_channels = [
            c.name for c in voice_channels if c.permissions_for(author).connect is True
        ]

        user_text_channels = [
            c.name for c in text_channels if c.permissions_for(user).read_messages is True
        ]
        user_voice_channels = [
            c.name for c in voice_channels if c.permissions_for(user).connect is True
        ]

        author_only_t = set(author_text_channels) - set(
            user_text_channels
        )  # text channels only the author has access to
        author_only_v = set(author_voice_channels) - set(
            user_voice_channels
        )  # voice channels only the author has access to

        user_only_t = set(user_text_channels) - set(
            author_text_channels
        )  # text channels only the user has access to
        user_only_v = set(user_voice_channels) - set(
            author_voice_channels
        )  # voice channels only the user has access to

        common_t = list(
            set(text_channels) - author_only_t - user_only_t
        )  # text channels that author and user have in common
        common_v = list(
            set(voice_channels) - author_only_v - user_only_v
        )  # voice channels that author and user have in common reboot

        msg = "```ini\n"
        msg += "{} [TEXT CHANNELS IN COMMON]:\n\n{}\n\n".format(
            len(common_t), ", ".join([c.name for c in common_t])
        )
        msg += "{} [TEXT CHANNELS {} HAS ACCESS TO THAT YOU DONT]:\n\n{}\n\n".format(
            len(user_only_t), user.name.upper(), ", ".join(list(user_only_t))
        )
        msg += "{} [TEXT CHANNELS YOU HAVE ACCESS TO THAT THEY DONT]:\n\n{}\n\n".format(
            len(author_only_t), ", ".join(list(author_only_t))
        )
        msg += "{} [VOICE CHANNELS IN COMMON]:\n\n{}\n\n".format(
            len(common_v), ", ".join([c.name for c in common_v])
        )
        msg += "{} [VOICE CHANNELS {} HAS ACCESS TO THAT YOU DONT]:\n\n{}\n\n".format(
            len(user_only_v), user.name.upper(), ", ".join(list(user_only_v))
        )
        msg += "{} [VOICE CHANNELS YOU HAVE ACCESS TO THAT THEY DONT]:\n\n{}\n\n".format(
            len(author_only_v), ", ".join(list(author_only_v))
        )
        msg += "```"
        await self.bot.say(msg)


 


    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        """Get a user's info (**BETA**)"""              
        if user == None:
            user = ctx.message.author
        adminrole = ['Admin' 'Sr admin']
        server = await self.bot.get_server(id=486910899756728320)
        role = discord.util.get(server.roles, name=adminrole)
        Dev = ['421698654189912064', '269340844438454272']
        Admins = discord.utils.get(server.members)     #https://tenor.com/view/ban-oprah-gif-10045949
        
        title="{}'s info".format(user.name)
        uinfo=discord.Embed(title=title, description="**User's ID:**\n{}".format(user.id), color=0xfac905)
        uinfo.add_field(name="Discriminator", value="{}".format(user.discriminator))
        uinfo.add_field(name="Avatar URL", value="[Click for preview (opens in browser)]({})".format(user.avatar_url))
        uinfo.add_field(name="Created at", value="{} UTC".format(user.created_at))

        
        
        #IF/ELSE stuff
        if discord.User.bot == True:
            uinfo.add_field(name="Is bot", value="True")
        

        if user.id in self.donators:
            uinfo.set_footer(text="Official donator!")
        else:
            pass
        if user.id == '517008210905923594':
            uinfo.set_footer(text="hey! thats me!")

        for x in server.members:
            if x in role:
                uinfo.set_footer(text="An official member | Rank: Admin")
            else:
                pass

        if user.id in Dev:
            uinfo.set_footer(text="An official member | Rank: Developer")
        uinfo.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=uinfo)

    @commands.command(aliases=['math', 'calc'], brief='Calculator. see -help calc for cool ascii.')
    async def calculate(self, number1: int = None, type: str = None,  number2: int = None):
        """ _____________________
            |  _________________  |
            | | 1 + 2           | |
            | |               3 | |
            | |_________________| |
            |  ___ ___ ___   ___  |
            | | 7 | 8 | 9 | | + | |
            | |___|___|___| |___| |
            | | 4 | 5 | 6 | | - | |
            | |___|___|___| |___| |
            | | 1 | 2 | 3 | | x | |
            | |___|___|___| |___| |
            | | . | 0 | = | | / | |
            | |___|___|___| |___| |
            |_____________________|
        """
        
        num1 = number1
        num2 = number2
        if type == '+':
            answer = num1 + num2
        if type == '-':
            answer = num1 - num2
        if type == '/':
            answer = num1 / num2
        if type == '*':
            answer = num1 * num2
        if type == '^':
            answer = num1 ^ num2

        a = "Input: {} {} {}\nOutput: `{}`".format(num1,type,num2,answer)
        await self.bot.say(a)   #new suggest

    

    @commands.command(pass_context=True)
    async def purge(self, ctx, number: int = 1):
        """purges x amount of messages from chat"""

        if ctx.message.author.server_permissions.manage_messages == True:
            await self.bot.delete_message(ctx.message)
            try:
                await self.bot.purge_from(ctx.message.channel, limit=number)
                logger.info('{} purged {}  messages from {}, {} ({})'.format(ctx.message.author, number, ctx.message.channel.name, discord.Server.name, discord.Server.id))
            except:
                try:
                    try:
                        counter = 0
                        async for x in self.bot.logs_from(ctx.message.channel, limit = number):
                            if counter < number:
                                try:
                                    try:
                                        await self.bot.delete_messages(x)
                                        counter += 1
                                        await asyncio.sleep(0.02)
                                    except:
                                        await self.bot.delete_message(x)
                                        counter += 1
                                        await asyncio.sleep(1.2)
                                except Exception as e:
                                    await self.bot.say(f"{e}")
                    except Exception as e:
                        await self.bot.say(f"error: ```py\n{e}\n```")
                except Exception as e:
                    await self.bot.say(f"error: ```py\n{e}\n```")
        else:
            await self.bot.say("Error: you do not have permission to manage messages")


        
        
        

    @commands.group(name="say",pass_context=True)
    async def say(self, ctx, *, msg: str):
        """Repeats whatever you say!"""
        fail = '<:fail:522076877075251201>'
        if ctx.invoked_subcommand is None:
            if msg == None:
                await self.bot.say("<:fail:522076877075251201> No msg arg was detected - Image uploads arent supported,"
                                   " if that's what you sent")
            else:
                try:
                    await self.bot.delete_message(ctx.message)
                    embed=discord.Embed(title="Message from {}".format(ctx.message.author), description=msg, color=0xfac905)
                    await self.bot.say(embed=embed)
                except Exception as e:
                    try:
                        embed=discord.Embed(title="Message from {}:".format(ctx.message.author), description=msg, color=0xfac905)
                        embed.set_footer(text=f"❌ An error occured while preforming this command:\n {e}")
                        await self.bot.say(embed=embed)
                    except Exception as error:
                        await self.bot.whisper(f"❌ i dont appear to have `embed links` permission, or `send messages`. your error: {error}."
                                                "\nTry running -perms <@517008210905923594> to see if i have them.")
        else:
            pass


        


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()   #Start recording the time to send a message
        message = await self.bot.say("Pinging...") #Showing its been registered
        ping = (time.monotonic() - before) * 1000 #get before - now (time to edit message)
        await self.bot.edit_message(message, f"Pong! `{int(ping)}ms`") #show the ping   stats

    @commands.command(name='8ball', aliases= ['8', 'ball'])
    async def ball(self, **question: str):
        """ask 8ball a question"""
        if question == 'am i gay':
            await self.bot.say("Certainly")
        if question == 'is EEK better then inside?':
            await self.bot.say("Certainly")
        
        
        
        bl = ["Definitly", "Yes", "Probably", "possibly", "unlikley", "Probably not", "no", "certainly not"]
        await self.bot.say(random.choice(bl))

    @commands.command(pass_context=True, aliases= ["info", "statistics"])
    async def stats(self, ctx):
        """get some statz"""
        servers = len(self.bot.servers)
        for i in self.bot.servers:
            for cid in i.channels:
                for dc in cid.id:
                    z = self.bot.get_channel(dc)
                    x = z
        users = len(set(self.bot.get_all_members()))
        owner = '421698654189912064'
        embed=discord.Embed(title="Server Count", description=servers, color=0xfac900)
        embed.add_field(name="Total users", value=users, inline=True)
        embed.add_field(name="Total channels", value=x)
        embed.add_field(name="created on", value="27th Nov 18")
        embed.add_field(name="Creator:", value="<@421698654189912064>")
        embed.add_field(name="bot list:", value="[click here](https://discordbotlist.com/bots/517008210905923594)")
        embed.add_field(name="Version", value="0.5 \|| beta ")


        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/FUiq-FAd9juVT2AidKJXACnbvOkt4n6vXRxJdSpJouc/%3Fsize%3D128/https/cdn.discordapp.com/avatars/517008210905923594/7a769765fda1fa7e9469d4bf6f3dbbf2.png")
        if ctx.invoked_subcommand is None:
            await self.bot.say(embed=embed)
        else:
            pass

# suggest
    @commands.command()
    async def news(self):
        """Get latest news"""
        # uTEXT = "**<update title>** : <vernum>:\n<text>"
        # TEXT = "[Title] : [vernum]:\n<text>"

        utext = "**Bug fixes and improvements** : v 0.6.2"
        
        text =  """
                this update mainly contains a few bug fixes and minor tweaks to commands.
                note: a few commands (like stats and userinfo) might not work because im currently in the process of updating them. If `-userinfo` **`channels`** content says `None`, please report it!
                anyways, not much to talk about, except the github is also somewhere you can put suggestions and bugs if the bot is down
                -EEK
                ----------
                **Embedded help!** : V0.6.1
                HELP IS NOW EMBEDDED THANK ME
                ok, i actually stole it from [red](https://discord.gg/red), and modified it to work with ebot, and made it look... *read-able* on mobile. Should you have any suggestions, feel free to -suggest with some info! im working on making it send to DM if the bot ends up not having perms
                -EEKIM10_YT (lead dev)
                ----------
                **suggest and calc** : V0.5.1.1
                -calc now functions properly, fixed a few bugs, and now displays differently.
                -suggest / -report now work, and now it is interactive! wow, reply much? just do -suggest and follow the bots instructions!
                laterz!
                -Ebot Dev Team | Ebot debug Team | EEKIM10_YT
                ----------
                **Calculator command and future updates** : v0.51\n
                -calc command has been added! (it is in alpha, so it will have issues for now).
                [You can also see our upcoming features](https://github.com/EEKIM10/cogs/projects/4), or the ones added [by our other dev](https://github.com/EEKIM10/cogs/projects/5).
                we also now have a debug channel, so**...**
                """

        embed=discord.Embed(title=utext, description=text, color=randint(0, 0xffffff))
        await self.bot.say(embed=embed)
#msg

    @commands.command()
    async def invite(self, type: str = None):    #saylol msg leaveserver suggest
        """Get support and links and stuff"""
        support = ['Support', 'support']
        invite = ['bot', 'invite', 'url']
        website = ['web', 'website', 'site']
        gh = ['git', 'github', 'repo']
        bl = ['botlist', 'list', 'bl']
        args = [gh, website, invite, support, bl]
        if type in support:
            e = discord.Embed(title="Support server:", description="[Click to get an invite](https://invite.gg/Ebot)",
                              color=0xffff00)
            await self.bot.say(embed=e)
            return
        if type in invite:
            e=discord.Embed(title="Invite", description="[Click for the invite](https://discordapp.com/api/oauth2/authorize?client_id=517008210905923594&permissions=0&redirect_uri=https%3A%2F%2Finvite.gg%2Febot&response_type=code&scope=bot%20identify)")
            await self.bot.say(embed=e)
            return
        if type in website:
            e = discord.Embed(title="website",description="[click here](https://sites.google.com/view/ebot-adiscordbot)")
            await self.bot.say(embed=e)
            return
        if type in gh:
            e = discord.Embed(title="GitHub Repo:",description="[im clickable, feel free](https://github.com/EEKIM10/cogs)")
            await self.bot.say(embed=e)
            return
        if type in bl:
            e = discord.Embed(title="Bot lists:", description="[1](https://discordboats.club/517008210905923594) [2](https://discordbotlist.com/517008210905923594)")
            await self.bot.say(embed=e)
            return
        if type == None:
            try:
                try:
                    e=discord.Embed(title="Support server:", description="[Click to get an invite](https://invite.gg/Ebot)", color=0xffff00)
                    e.add_field(name="Invite", value="[Click for the invite](https://discordapp.com/api/oauth2/authorize?client_id=517008210905923594&permissions=0&redirect_uri=https%3A%2F%2Finvite.gg%2Febot&response_type=code&scope=bot%20identify)")
                    e.add_field(name="Bot List:", value="retired. please join support server and go to #info", inline=False)
                    e.add_field(name="website:", value="[click here](https://sites.google.com/view/ebot-adiscordbot)", inline=False)
                    e.add_field(name="GitHub Repo:", value="[im clickable, feel free](https://github.com/EEKIM10/cogs)", inline=False)

                    await self.bot.say(embed=e)
                except discord.Forbidden:
                    await self.bot.say("great `embed links` permission i have here. its so good it isnt even enabled! (please enable this first)_")
            except Exception as e:
                await self.bot.say(f"an error occured. please report error in the support server (<https://invite.gg/Ebot>) FYI, this was the error: `{e}`` (please reference this string of code in support)")
            return
        if type not in args:
            await self.bot.say("invalid arg passed. valid arguments: `Support | support | bot | invite | url | web |"
                               "website | site | git | github | repo | botlist | list | bl`\nOr leave args blank [`-invite`]")

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices : str):
        """Chooses between multiple choices."""
        await self.bot.say("I choose `{}`".format(random.choice(choices)))


    @commands.command()
    async def credits(self):
        """Get credits to people who in/directly contributed to making this bot"""
        ce=discord.Embed(Title="Special thanks to:", description="EEKIM10_YT (making the bot, lead developer)\n[The red community](https://discord.gg/red) (debugging)"
        "\nAikaterna (commonly responded with helpful info and criticism)\nPEᑎGᑌIᑎ114 (motivation, Server Admin, great friend)\nPeople on github (didnt do much, but might as well include them\n"
        "InsideDev (fuck mee6 emoji, ideas)\nStackoverflow (no idea how many times this has saved my skin)",color=0xfac905)
        ce.set_footer(text="thank you for helping the development of Ebot!")
        ce.add_field(name="Developers", value="EEKIM10_YT (lead dev, founder)\nShiatryx (dev, lead debugger)")
        ce.set_thumbnail(url="https://cdn.discordapp.com/avatars/517008210905923594/7a769765fda1fa7e9469d4bf6f3dbbf2.webp?size=1024")
        await self.bot.say(embed=ce)

    @commands.command(pass_context=True, aliases= ['randomnumbergenerator', 'randomnum'])
    async def rng(self, ctx, number: int = None, other_number: int = None):
        """Pull a random number\nE.g:\n-rng 100 200"""

        #alright lets break my brain
        if number == 0 or None:
            number = 1
        
        if other_number == 0 or None:
            other_number = 101

        #Now for generating the number       post        reboot
        try:
            try:
                embed=discord.Embed(title="Your random number:", description="-",color=0xfffff0)
                embed2=discord.Embed(title="Your random number:", description="/",color=0xff7100)
                embed3=discord.Embed(title="Your random number:", description=randint(number, other_number), color=0xfac905)
                msg = await self.bot.say(embed=embed)
                await asyncio.sleep(1)
                await self.bot.edit_message(msg, embed=embed2)
                await asyncio.sleep(2)
                await self.bot.edit_message(msg, embed=embed3)
            except Exception as f:
                await self.bot.say(f"```py\n{f}\n```")
        except Exception as f:
            await self.bot.say(f"```py\n{f}\n```") 


    @commands.command(pass_context=True)
    async def suggest(self,ctx, *,desc: str):
        """info on how to suggest something"""

        yes = discord.Emoji
    
        e=discord.Embed(title='Suggestion', description=desc, color=randint(0, 0xffffff))
        
        await self.bot.say("If the suggestion is made, the bot will send a message to this channel, to send to a custom channel, reply with its ID within 20s"
        "\nNote: If you dont want a custom channel, put `None`")
        
        c = await self.bot.wait_for_message(timeout=20, author=ctx.message.author, channel=ctx.message.channel)
        n = ['None', 'none']
        if c == None:
            pass
        if c.content in n:
            v="<#{}>".format(ctx.message.channel.id)
            e.add_field(name="Custom channel ID:", value=v)
        else:
            v=c.content
            e.add_field(name="Custom channel ID:", value=v)
       
       
        e.set_footer(text=f'Author: {ctx.message.author}, {ctx.message.author.id} || server: {ctx.message.server.name}, {ctx.message.server.id}')
        
        
        if v == ctx.message.channel.id:
            await self.bot.say("Sent. You will recieve a reply in this channel, if you would like to change it, reply "
                        "`delete` within 30s, or 'confirm' to skip.")
        else:
            await self.bot.say(f"Sent. You will recieve a reply in '{v}', if you would like to change it, reply "
                        "`delete` within 30s, or 'confirm' to skip.")
        c = await self.bot.wait_for_message(timeout=30, author=ctx.message.author, channel=ctx.message.channel)
        if c == None:
            await self.bot.say("You have not replied 'delete'. Your message has been sent and now can not be deleted. to view it, join -invite")
            msg = await self.bot.send_message(discord.Object(id=543767237656576011), "<@&538410984411234324>, {}".format(embed=e))
            
            await self.bot.add_reaction(message=msg,emoji="success:522078924432343040")
            return
        if c.content == 'delete':
            await self.bot.delete_message(msg)
            await self.bot.say("removed. here was your content:\n```md\n{}\n```".format(desc))
        if c.content == 'confirm':
            await self.bot.say("Alright, the suggestion can nolonger be deleted.")
            pmsg = await self.bot.send_message(discord.Object(id=543767237656576011), "<@&538410984411234324>")
            msg = await self.bot.send_message(discord.Object(id=543767237656576011), embed=e)
            await self.bot.add_reaction(message=msg,emoji="success:522078924432343040")
            await self.bot.add_reaction(message=msg, emoji="fail:522076877075251201")

    @commands.command(pass_context=True)
    async def report(self, bug: str):
        """Report a bug/server!"""


    @commands.command()
    @checks.admin_or_permissions(manage_roles=True)
    async def mperms(self):
        """List the minimum perms for the bot"""
        list = """
        Send & read, read msg history
        manage messages
        **create instant invite**
        kick members
        manage roles
        **embed links**
        use external emojis
        """
        embed = discord.Embed(title="minimum perms:", description=list,color=0xfac905)
        embed.set_footer(text="Text in bold is required and if not provided will be an instant serverban.")
        try:
            await self.bot.say(embed=embed)
        except:
            try:
                await self.bot.say(list)
            except:
                try:
                    await self.bot.whisper("give me send messages dude. Below is the list of minimum permissions")
                    await self.bot.whisper(list)
                except:
                    return

    
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        """Get server's info"""
        embed=discord.Embed(title=f"{ctx.message.server.name}'s info:", description="ID:{}".format(ctx.message.server.id), color=randint(0, 0xffffff))
        for roles in ctx.message.server.roles:
            roles = roles.name












#userinfo   suggest eval

# OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC 
#OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC 
#vOC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC OC 



def setup(bot):
    n = CoreCommands(bot)       
    bot.add_cog(n)