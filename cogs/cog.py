
import random
from random import randint
import asyncio
import logging
import time
import discord
import os
import collections
import datetime
from .utils import checks
from discord.ext import commands
from cogs.utils.pagify import pagify, box


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
        self.donators = ['421698654189912064', '415912795574501386', '344878404991975427', '269340844438454272',
                         '293066151695482882', '493790026115579905', '365659613821009920']
        self.emoji_list = {
            "startemoji": '⏮',
            "backemoji": '⏪',
            "closeemoji": '⏹',
            "nextemoji": '⏩',
            "endemoji": '⏭'
        }
        self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z']


    @commands.command(name='help', pass_context=True, aliases=['?', 'h'])
    async def _help(self, ctx, command = None):
        """Embedded help command"""
        author = ctx.message.author
        num = 0
        if not command:
            msg = "**Command list:**"
            color = randint(0, 0xffffff)


            final_coms = {}
            com_groups = []
            for com in self.bot.commands:
                try:
                    if not self.bot.commands[com].can_run(ctx):
                        continue
                    else:
                        num += 1
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
                    em.set_thumbnail(url='https://images-ext-1.discordapp.net/external/YOvQKXSB5j-dOJ_7U7HUnoCi6nyX5LRNq9X38ls8slk/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/517008210905923594/7a769765fda1fa7e9469d4bf6f3dbbf2.webp?width=521&height=521')

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
                em.set_footer(text=f"{num} commands!")

                if field_count == 15 or is_last:
                    to_send.append(em)
                    field_count = 0


        
            try:
                await self.bot.say(embed=em)
            except discord.Forbidden:
                a = await self.bot.say("I was forbidden from sending embeds. If you would like to see my commands list"
                                       " reply `yes` within 10s. P.S: please notify an admin to give me minimum perms @"
                                       " -mperms, as if not it could result in a serverban.")
                m = await self.bot.wait_for_message(timeout=15, author=author, channel=ctx.message.channel)
                msg = m.content
                y = ['y', 'Y', 'Yes', 'yes']
                if msg == None:
                    await self.bot.delete(ctx.message)
                    await self.bot.delete_message(a)
                    await self.bot.delete_message(m)
                elif msg in y:
                    await self.bot.edit_message(a, "Sending to DMs...")
                    try:
                        await self.bot.whisper(embed=em)
                        await self.bot.edit_message(a, "Sent to DMs")
                    except discord.Forbidden:
                        await self.bot.edit_message(a, "Unable to send to DMs.")
                else:
                    await self.bot.edit_message(a, "`else` trigger placeholder")
        else:
            msg = "**Command Help:**"
            color = randint(0, 0xffffff)

            em=discord.Embed(description=msg,
                             color=color)
            try:
                if not self.bot.commands[command].can_run(ctx):
                    await self.bot.say("This command is locked behind acheck you don't meet.")
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
                await self.bot.say("searching...")
                await asyncio.sleep(randint(1, 3))
                await self.bot.say(f"Couldn't find {command} as a registered command!")


    async def on_server_join(self,server):
        jembed=discord.Embed(title="I joined {}!".format(server), description="Now in {} servers (on this shard)!".format(len(self.bot.servers)), color=randint(0,0xffffff))
        jembed.add_field(name="Members", value=server.member_count)
        jembed.add_field(name="owner",value=server.owner)
        jembed.add_field(name="region", value=server.region)
        jembed.set_footer(text=server.id)
        jembed.set_thumbnail(url="{}".format(server.icon_url))
        banned = ['504050383338078229', '526438179574906881', '504539562861789204']
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
                await self.bot.send_message(ctx.message.channel, "Command is on cooldown!\nRetry-in: `{}`s".format(round(error.retry_after)))
                return
            if isinstance(error, discord.ext.commands.errors.CheckFailure):
                pass
        if isinstance(error, ZeroDivisionError):
            await self.bot.say("ZeroDivisionErrorHandled = True - cannot divide by 0")

        else:
            e = error
            e = discord.Embed(title="<:fail:522076877075251201> Unhandled Error:", description=f"```\n{error}\n```", color=0xff2b2b)
            e.add_field(name="How to fix:", value="Please report this [to my developer](https://invite.gg/Ebot) or [open an issue on github](https://github.com/EEKIM10/cogs/issues/new)")
            try:
                await self.bot.send_message(ctx.message.channel, embed=e)
            except:
                await self.bot.send_message(ctx.message.channel, f"```py\n{error}\n```")
            finally:
                raise error




    #ping       purge       userinfo    invite  serverinfo  news

    @commands.command(pass_context=True)
    async def quote(self, ctx, message_id, channel_id: int = None):
        """Get a quote from a message ID"""
        if channel_id == None:
            channel = ctx.message.channel
        else:
            channel = discord.Object(id=channel_id)
        try:
            msg = await self.bot.get_message(channel=channel, id=message_id)
            cntnt = msg.content
            gembed = discord.Embed(title="Message from {}".format(msg.author.name), description=f"```md\n{cntnt}\n```", color=randint(0, 0xffffff))
            await self.bot.say(embed=gembed)
        except (discord.NotFound, discord.HTTPException, discord.Forbidden) as e:
            await self.bot.say(f"```py\n{e}\n```")

    @commands.command()
    async def shoot(self, user: discord.Member):
        """shoot someone"""
        await self.bot.say(f"Shot {user.mention}.")


    
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
    async def userinfo(self, ctx, user: discord.User = None):
        """Get a user's info (**BETA**)"""              
        if user == None:
            user = ctx.message.author
        server = self.bot.get_server(id=486910899756728320)
        Dev = ['421698654189912064', '269340844438454272']
        # https://tenor.com/view/ban-oprah-gif-10045949
        status = discord.Status
        
        title="{}'s info".format(user.name)
        uinfo=discord.Embed(title=title, description="**User's ID:**\n{}".format(user.id), color=0xfac905)
        uinfo.add_field(name="Discriminator", value="{}".format(user.discriminator))
        uinfo.add_field(name="Avatar URL", value="[Click for preview (opens in browser)]({})".format(user.avatar_url))
        uinfo.add_field(name="Created at", value="{} UTC".format(user.created_at))
        if user.bot:
            uinfo.add_field(name="Is bot:",value="True")
        else:
            uinfo.add_field(name="Is bot:", value="false")
        if user.status == status.offline:
            s = "Offline"
        if user.status == status.dnd:
            s = "Do not disturb"
        if user.status == status.idle:
            s = "Idle/AFK"
        if user.status == status.online:
            s = "Online"

        uinfo.add_field(name="status:", value=s)


        
        
        #IF/ELSE stuf
        mut = 0
        if ctx.message.author.id in self.donators:
            for server in self.bot.servers:
                for member in server.members:
                    if member.id == user.id and ctx.message.author.id:
                        mut += 1
            uinfo.add_field(name="Mutual servers", value=f"{mut} (in the servers im in too)")
        if user.id in self.donators:
            uinfo.set_footer(text="Official donator!")
        elif user.id == '517008210905923594':
            uinfo.set_footer(text="hey! thats me!")
        elif user.id in Dev:
            uinfo.set_footer(text="An official member | Rank: Developer")
        uinfo.set_thumbnail(url=user.avatar_url)
        await self.bot.say(embed=uinfo)

    @commands.command(aliases=['math', 'calc'], brief='Calculator. see -help calc for cool ascii.')
    async def calculate(self, number1: int = None, type: str = None,  number2: int = None, rounded: str = False):
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
        if number2 == 0:
            await self.bot.say("Cannot divide by zero. dividing by 2...")

            number2 += 2
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

        if rounded == False:
            a = "Input: {} {} {}\nOutput: `{}`".format(num1,type,num2,answer)
            await self.bot.say(a)   #new suggest
        elif rounded == True:
            a = "Input: {} {} {}\nOutput: `{}`".format(num1,type,num2,round(answer))
            await self.bot.say(a)
        else:
            await self.bot.say("Error: `rounded` arg has to be either `True` or `False`.")

    

    @commands.command(pass_context=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @checks.mod_or_permissions(manage_messages=True)
    async def purge(self, ctx, number: int = 1):
        """purges x amount of messages from chat"""

        if ctx.message.author.server_permissions.manage_messages == True:
            await self.bot.delete_message(ctx.message)
            try:
                await self.bot.purge_from(ctx.message.channel, limit=number)
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
    @commands.cooldown(1, 3, commands.BucketType.channel)
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
        one = time.monotonic()
        msg = await self.bot.say("Gathering stats...")
        rn = randint(0, 9999)
        rl = random.choice(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
        'j', 'k', 'l', 'm', 'n', 'o', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'])
        servers = len(self.bot.servers)
        channels = len(set(self.bot.get_all_channels()))
        users = len(set(self.bot.get_all_members()))
        owner = '421698654189912064'
        embed=discord.Embed(title="Server Count", description=servers, color=0xfac900)
        embed.add_field(name="Total users", value=users, inline=True)
        embed.add_field(name="Total channels", value=channels)
        embed.add_field(name="created on", value="27th Nov 18")
        embed.add_field(name="Creator:", value="<@421698654189912064>")
        embed.add_field(name="bot list:", value="Type `-invite bl`.")
        embed.add_field(name="Version", value="0.5 \|| beta ")
        x = f"And heres a random number, because why not {rn}"
        y = f"And heres a random letter, because i like l3tters: {rl}"
        topick = [x, y]
        embed.set_footer(text=random.choice(topick))

        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/FUiq-FAd9juVT2AidKJXACnbvOkt4n6vXRxJdSpJouc/%3Fsize%3D128/https/cdn.discordapp.com/avatars/517008210905923594/7a769765fda1fa7e9469d4bf6f3dbbf2.png")
        two = time.monotonic()
        if ctx.invoked_subcommand is None:
            msg2 = "got all stats - {}s".format(round(one - two))
            await self.bot.edit_message(msg, msg2, embed=embed)
        else:
            pass

# suggest
    @commands.command()
    async def news(self):
        """Get latest news"""
        # uTEXT = "**<update title>** : <vernum>:\n<text>"
        # TEXT = "[Title] : [vernum]:\n<text>"

        utext = "**ServerInfo!** : v 0.6.3"
        
        text =  """
                The long awaited `serverinfo` command is here! its in beta, but includes features (as of 17/2):
                • Server ID
                • Member list
                • bot : user ratio
                • role list
                • server owner mention
                • all roles
                • server creation date
                • icon url
                • ~50 lines of code
                and much more to come! it will be the current focus of the bot for now, until ive packed everything in it as i can!
                anyways, l8rs!
                -EEEEEEEEEEEEEEEEEEEEEEEEEEK
                ----------
                **Bug fixes and improvements** : v 0.6.2
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
                -sugges **[...](https://cdn.discordapp.com/attachments/538441181562929172/546775043326214144/image0.png)**
                """

        embed=discord.Embed(title=utext, description=text, color=randint(0, 0xffffff))
        try:
            await self.bot.say(embed=embed)
        except discord.HTTPException:
            await self.bot.say("I cant send the message, its probably too long. ask my dev to shorten it.")
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
        ce.set_thumbnail(url=self.bot.avatar_url)
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
    @commands.cooldown(1, 120, commands.BucketType.user)
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
            msg = await self.bot.send_message(discord.Object(id=543767237656576011), "<@&538410984411234324> <@&544915113719889965> {}".format(embed=e))
            
            await self.bot.add_reaction(message=msg,emoji="success:522078924432343040")
            return
        if c.content == 'delete':
            await self.bot.delete_message(msg)
            await self.bot.say("removed. here was your content:\n```md\n{}\n```".format(desc))
        if c.content == 'confirm':
            await self.bot.say("Alright, the suggestion can nolonger be deleted.")
            pmsg = await self.bot.send_message(discord.Object(id=543767237656576011), "<@&538410984411234324> <@&544915113719889965>")
            msg = await self.bot.send_message(discord.Object(id=543767237656576011), embed=e)
            await self.bot.add_reaction(message=msg,emoji="success:522078924432343040")
            await self.bot.add_reaction(message=msg, emoji="fail:522076877075251201")

    @commands.command(pass_context=True)
    async def report(self, bug: str):
        """Report a bug/server!"""


    @commands.command()
    @checks.admin_or_permissions(manage_roles=True)
    async def mperms(self, missing: str = None):
        """List the minimum perms for the bot"""
        if missing is None or 'false':
            list = """
            Send & read, read msg history
            manage messages
            create instant invite
            manage roles
            embed links
            use external emojis
            """
            embed = discord.Embed(title="minimum perms:", description=list,color=0xfac905)
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
        else:
            list = ""
            m = ['']
            if ctx.server.me.server_permissions.send_messages is False:
                list += "Missing: send_messages"
                m.append('send-m')
            embed = discord.Embed(title="minimum perms:", description=list, color=0xfac905)
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

    @commands.command()
    async def coinflip(self, bet: str):
        """flip a coin"""
        sides = ['heads!', 'side!', 'tails!']
        side = random.choice(sides)
        if bet == side:
            win = True
        else:
            win = False
        if side == 'side':
            side = "on it's side!"
        if win == True:
            w = discord.Embed(title="Flipped!", description="landed on {side}\nYou won :D", color=0xe75252,
                              timestamp=datetime.datetime.now())
            await self.bot.say(embed=w)
        else:
            w = discord.Embed(title="Flipped!", description="landed on {side}\nYou lost :C", color=0xe75252,
                              timestamp=datetime.datetime.now())
            await self.bot.say(embed=w)
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        """Get server's info"""
        a = await self.bot.say("Gathering stats...")
        startemoji = '⏮'
        backemoji = '⏪'
        closeemoji = '⏹'
        nextemoji = '⏩'
        endemoji = '⏭'
        server = ctx.message.server
        bc = 0
        userc = 0
        for user in server.members:
            if user.bot:
                bc += 1
            else:
                userc += 1
        total = userc + bc
        roles = " "
        for role in ctx.message.server.roles:
                    roles += (f"{role.mention}\n")
        o = [discord.Status.online, discord.Status.idle, discord.Status.do_not_disturb]
        ol = 0
        of = 0
        for user in server.members:
            if user.bot:
                pass
            else:
                if user.status in o:
                    ol += 1
                else:
                    of += 1

        e = discord.Embed(title=f"{server.name}'s info:", description=f"Server ID: {server.id}", color=randint(0, 0xffffff))
        e.add_field(name="Members:", value=f"Bots: {bc} | Users: {userc} | total: {total} (may be inaccurate)", inline=False)
        e.add_field(name="owner:", value=server.owner.name, inline=False)
        e.add_field(name="Created at:", value=server.created_at)
        e.add_field(name="Roles:", value=roles, inline=False)
        e.add_field(name="online : offline users ratio:", value=f"{ol}:{of}")
        e.set_thumbnail(url=server.icon_url)
        e.set_footer(text="Ebot server info | BETA | react with arrows to navigate!")

        e2 = discord.Embed(title=f"{server.name}'s role list:", description=roles)
        try:
            msg = await self.bot.say(embed=e)
            await self.bot.delete_message(a)
            #await self.bot.add_reaction(msg, closeemoji)
            #await self.bot.add_reaction(msg, nextemoji)
            #a = await self.bot.wait_for_reaction(timeout=60)
            #if a == None:
             #   await self.bot.clear_reactions(msg)
            #elif a.reaction == closeemoji:
            #    await self.bot.delete_message(msg)
            #else:
            #    await self.bot.edit_message(msg, embed=e2)
            #    await self.bot.say("Beta - end of reaction menue.")


        except discord.HTTPException:
            e.remove_field(4)
            await self.bot.say(embed=e)


    @commands.command(pass_context=True)
    async def check(self, ctx, user: discord.Member = None):
        """checks what perms you/user has/ve and spits it out in a nice embed. premium only."""
        message = ctx.message
        if user == None:
            author = message.author
        else:
            author = user
        perms = author.server_permissions
        msg = " "
        e = discord.Embed(title=f"Permissions for {author.name}", value="None", color=randint(0, 0xffffff))
        if ctx.message.author.id in self.donators:
            g = await self.bot.say("Gathering General Permissions...")
            if perms.administrator == True:
                msg += "Administrator = `True`\n"
            else:
                msg += "Administrator = `False`\n"
            if perms.manage_server == True:
                msg += "Manage Server = `True`\n"
            else:
                msg += "Manage Server = `False`\n"
            if perms.manage_channels == True:
                msg += "Manage Channels = `True`\n"
            else:
                msg += "Manage Channels = `False`\n"
            if perms.manage_roles == True:
                msg += "Manage Roles = `True`\n"
            else:
                msg += "Manage Roles = `False`\n"
            if perms.kick_members == True:
                msg += "Kick Members = `True`\n"
            else:
                msg += "Kick Members = `False`\n"
            if perms.ban_members == True:
                msg += "Ban Members = `True`\n"
            else:
                msg += "ban Members = `False`\n"
            if perms.create_instant_invite == True:
                msg += "Gen Invite = `True`\n"
            else:
                msg += "Gen Invite = `False`\n"
            if perms.change_nickname == True:
                msg += "Change Nickname = `True`\n"
            else:
                msg += "Change Nickname = `False`\n"
            if perms.manage_nicknames == True:
                msg += "Manage nicks = `True`\n"
            else:
                msg += "Manage nicks = `false`\n"
            if perms.manage_emojis == True:
                msg += "manage emojis = `True`\n"
            else:
                msg += "Manage emojis = `false`\n"
            await self.bot.edit_message(g, "Gathered General perms, moving to text...")
            e.add_field(name="General permissions", value=msg, inline = False)
            await self.bot.say("End of Perms command (beta). Heres the current value:", embed=e)


        else:
            await self.bot.say("Premium only! Join the support server for info.")








    @commands.command(pass_context=True)
    async def list(self, ctx, type: str = None):
        """get a list of users/roles/channels"""
        msg = " "
        if type == None:
            list1 = ctx.message.server.members
            for member in list1:
                msg += f"{member.name} | {member.id}"
            for page in pagify:
                await self.bot.say(page(msg))
        elif type == 'users':
            list2 = ctx.message.server.members
            type = list2
            for member in list2:
                msg += f"{member.name} | {member.id}"
            for page in pagify:
                await self.bot.say(page(msg))
        elif type == 'roles':
            list3 = ctx.message.server.roles
            for role in list3:
                msg += f"{role.name} | {role.id}"
            for page in pagify:
                await self.bot.say(page(msg))
        elif type == 'channels':
            list4 = ctx.message.server.channels
            for channel in list4:
                msg += f"{channel.name} | {channel.id}"
            for page in pagify:
                await self.bot.say(page(msg))
        else:
            await self.bot.say("Invalid type passed - must be any of the following:\n"
                               "`channels` `roles` `users` `None`")
            return

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def announce(self, ctx):
        """announce a message in a #channel"""
        msg = ctx.message
        author = msg.author
        channel = msg.channel
        dele = await self.bot.delete_message(ctx.message)
        emb = 0
        ev = 0
        he = 0
        ed = 0
        id = 0
        foot = "Embedded announcement by ebot 2.0 | "
        rm = ""
        # basic I/O yes i know shut up
        title = ""
        desc = ""
        ned = f"```announcement from {author.name}:```"

        y = ['Yes', 'yes', 'y', 'Y']
        canc = ['Cancel', 'cancel']
        code = randint(0, 9999)

        a = await self.bot.say("Please say your selections for the message. say `finish` to finish customisation,"
                               " and move on to the main body of the text you will send. say `args` for valid"
                               " arguments.")
        #grabbing options
        while True:
            b = await self.bot.wait_for_message(author=author, channel=channel)
            c = b.content
            if c == 'finish':
                await self.bot.delete_message(b)
                break
            elif c == 'args':
                await self.bot.delete_message(b)
                await self.bot.edit_message(a, "Valid arguments: `embed`, `here`, `everyone` or `rolemention`.\nps:"
                                               " returning to arg selection in 5s")
                await asyncio.sleep(5)
                await self.bot.edit_message(a, "Please say your selections for the message. say `finish` to finish "
                                               "customisation,"
                                               " and move on to the main body of the text you will send. "
                                               "say `args` for valid"
                                               " arguments.")
            elif c == 'embed':
                emb += 1
                await self.bot.delete_message(b)
            elif c == 'here':
                he += 1
                await self.bot.delete_message(b)
            elif c == 'everyone':
                ev += 1
                await self.bot.delete_message(b)
            elif c == 'rolemention':
                await self.bot.edit_message(a, "please give me an id, name or mention the role to mention.")
                r = await self.bot.wait_for_message(author=author, channel=channel)
                await self.bot.delete_message(r)
                await self.bot.edit_message(a, "Please say your selections for the message. say `finish` to finish "
                                               "customisation,"
                                               " and move on to the main body of the text you will send. "
                                               "say `args` for valid"
                                               " arguments.")
                for role in r.role_mentions:
                    if role == None or 0:
                        pass
                    else:
                        rm += role.mention
                if rm == "":
                    rm = discord.utils.get(ctx.message.server.roles, name=r.content)
                    if rm == None:
                        pass
                    else:
                        rm = rm.mention
                if rm == None:
                    rm += "<@&{}>".format(r.content)

        # Embed gen
        if emb == 1:
            await self.bot.edit_message(a, "Embed: 1 - please reply with a title...")
            b = await self.bot.wait_for_message(author=author, channel=channel)
            title += b.content
            await self.bot.delete_message(b)
            await self.bot.edit_message(a, "... a description...")
            b = await self.bot.wait_for_message(author=author, channel=channel)
            desc += b.content
            await self.bot.delete_message(b)
            await self.bot.edit_message(a, "...reply with footer. say `None` to leave blank")
            b = await self.bot.wait_for_message(author=author, channel=channel)
            if b.content == 'None':
                pass
            else:
                foot += (str(b.content))


            ed += 1
        else:
            pass

        # getting main body
        if ed == 0:
            await self.bot.edit_message(a, "please tell me what to say.")
            b = await self.bot.wait_for_message(author=author, channel=channel)
            ned += b.content
            await self.bot.delete_message(b)
        else:
            pass
        #sending
        await self.bot.edit_message(a, "Please mention a channel or provide me an id.")
        e = await self.bot.wait_for_message(author=author, channel=channel)
        for c in e.channel_mentions:
            id += int(c.id)
            break
        if id == 0:
            id = int(e.content)
        await self.bot.delete_message(e)

        # actually SENDING
        embe = discord.Embed(title=title, description=desc, color=randint(0, 0xffffff), timestamp=datetime.datetime.now())
        embe.set_author(icon_url=author.avatar_url, name=author.name)
        if foot == "":
            pass
        else:
            embe.set_footer(text=foot)
        if ev == 1:
            if emb == 1:
                await self.bot.send_message(discord.Object(id=id), content="@everyone", embed=embe)
                await self.bot.edit_message(a, "Sent announcement successfully.")
            else:
                await self.bot.send_message(discord.Object(id=id), content=f"@everyone\n{ned}")
                await self.bot.edit_message(a, "Sent announcement successfully.")
        elif he == 1:
            if emb == 1:
                await self.bot.send_message(discord.Object(id=id), content="@here", embed=embe)
                await self.bot.edit_message(a, "Sent announcement successfully.")
            else:
                await self.bot.send_message(discord.Object(id=id), content=f"@here\n{ned}")
                await self.bot.edit_message(a, "Sent announcement successfully.")
        elif rm != "":
            if emb == 1:
                await self.bot.send_message(discord.Object(id=id), content=rm, embed=embe)
                await self.bot.edit_message(a, "Sent announcement successfully.")
            else:
                await self.bot.send_message(discord.Object(id=id), content=f"{rm}\n{ned}")
                await self.bot.edit_message(a, "Sent announcement successfully.")
        else:
            if emb == 1:
                await self.bot.send_message(discord.Object(id=id), embed=embe)
                await self.bot.edit_message(a, "Sent announcement successfully.")
            else:
                await self.bot.send_message(discord.Object(id=id), f"{ned}")
                await self.bot.edit_message(a, "Sent announcement successfully.")









    @commands.command()
    async def randomhex(self):
        """Generates a random Hex color"""
        color = randint(0, 0xffffff)
        embed = discord.Embed(description=f"Hex value: #{color}. Preview in embed bar", color=color)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 600, commands.BucketType.server)
    async def bump(self, ctx):
        """Bump Ye server. Premium only"""
        if ctx.message.author.id in self.donators:
            bumpedto = 0
            server = ctx.message.server
            invite = ""
            p = await self.bot.say("Grabbing server invite(s) <a:loading:551413963766890527>")
            #getting invites
            inviteobject = await self.bot.invites_from(server)
            for invite in inviteobject:
                if invite.max_age and invite.max_uses == 0:
                    invite = f"https://discord.gg/{invite.code}"
                    break
                else:
                    pass
            if invite == "":
                for channel in ctx.message.server.channels:
                    try:
                        invitet = await self.bot.create_invite(channel, max_age=0, max_uses=0, unique=False)
                        invite += invitet.url
                        break
                    except:
                        continue
            else:
                pass


            a = await self.bot.edit_message(p, "Grabbing server icon, owner, name, bump message & channel, "
                                               "and member count <a:loading:551413963766890527>")
            # getting bump msg from channel topic
            channelcount = 0
            for channel in ctx.message.server.channels:
                if channel.name == 'bump':
                    bumpchannel = channel
                    channelcount += 1
                    if channel.topic == None:
                        await self.bot.say("Error: No bump message detected. ensure it is in the channel's topic.")
                        return
                    else:
                        bumpmsg = bumpchannel.topic
                else:
                    pass
            if channelcount == 0:
                await self.bot.edit_message(a, "No bump channel(s) have been dected.")
                return False
            else:
                pass
            #getting all members and diff bots and humans
            bots = 0
            humans = 0
            for member in server.members:
                if member.bot == True:
                    bots += 1
                else:
                    humans += 1
            #sending to all servers with a channel called "bump":
            bumpable = 0
            fails = ""
            for server in self.bot.servers:
                for channel in server.channels:
                    if channel.name == 'bump':
                        bumpable += 1
                        await self.bot.edit_message(a, "Generating embed <a:loading:551413963766890527>")
                        await asyncio.sleep(1)
                        embed = discord.Embed(title=f"{ctx.message.server.name}", description=bumpmsg, color=randint(0,0xffffff))
                        embed.add_field(name="Info:", value=f"Owner: {ctx.message.server.owner}\n" \
                            f"Bots: {bots} | Humans: {humans}\nchannels: {len(ctx.message.server.channels)}\n"
                        f"Roles: {len(ctx.message.server.roles)}\n Invite code: {invite}")
                        await self.bot.edit_message(a, f"sending to {server.name} <a:loading:551413963766890527>")
                        embed.set_thumbnail(url=ctx.message.server.icon_url)
                        try:
                            await self.bot.send_message(channel, embed=embed)
                            try:
                                await self.bot.send_file(channel, "rainbow.gif")
                            except:
                                pass
                            await self.bot.edit_message(a, f"Sent to {server.name} <:success:522078924432343040>")
                            await asyncio.sleep(1)
                            bumpedto += 1
                        except Exception as e:
                            await self.bot.edit_message(a, f"Failed to message {server.name} <:fail:522076877075251201>")
                            fails += f"```py\n{e}\n```\n"
                        await asyncio.sleep(1)
            if fails == "":
                pass
            else:
                for p in pagify(fails):
                    await self.bot.say(f"Failed to send to some server(s):\n{p}")

            await self.bot.edit_message(a, f"Complete. bumped to: `{bumpedto}/{bumpable}/{len(self.bot.servers)}` "
            f"(bumped to/bumpable servers/all servers)")
        else:
            await self.bot.say("Donator only")

    @commands.command(pass_context=True, aliases=['bp', 'p', 'preview'])
    async def bumppreview(self, ctx):
        """preview your bump message"""
        bumpedto = 0
        server = ctx.message.server
        invite = ""
        p = await self.bot.say("Grabbing server invite(s)")
        # getting invites
        inviteobject = await self.bot.invites_from(server)
        for invite in inviteobject:
            if invite.max_age and invite.max_uses == 0:
                invite = f"https://discord.gg/{invite.code}"
                break
            else:
                pass
        if invite == "":
            for channel in ctx.message.server.channels:
                try:
                    invitet = await self.bot.create_invite(channel, max_age=0, max_uses=0, unique=False)
                    invite += invitet.url
                    break
                except:
                    continue
        else:
            pass
        a = await self.bot.edit_message(p,
                                        "Grabbing server icon, owner, name, bump message & channel, and member count")
        # getting bump msg from channel topic
        channelcount = 0
        for channel in ctx.message.server.channels:
            if channel.name == 'bump':
                bumpchannel = channel
                channelcount += 1
                if channel.topic == None:
                    await self.bot.say("Error: No bump message detected. ensure it is in the channel's topic.")
                    return
                else:
                    bumpmsg = bumpchannel.topic
            else:
                pass
        if channelcount == 0:
            await self.bot.edit_message(a, "No bump channel(s) have been dected.")
            return False
        else:
            pass
        # getting all members and diff bots and humans
        bots = 0
        humans = 0
        for member in server.members:
            if member.bot == True:
                bots += 1
            else:
                humans += 1
        # sending to all servers with a channel called "bump":
        bumpable = 0
        fails = ""
        await self.bot.edit_message(a, "Generating embed")
        await asyncio.sleep(1)
        embed = discord.Embed(title=f"{ctx.message.server.name}", description=bumpmsg,
                              color=randint(0, 0xffffff))
        embed.add_field(name="Info:", value=f"Owner: {ctx.message.server.owner}\n" \
            f"Bots: {bots} | Humans: {humans}\nchannels: {len(ctx.message.server.channels)}\n"
        f"Roles: {len(ctx.message.server.roles)}\n Invite code: {invite}")
        await self.bot.edit_message(a, f"Generating embed - preparing to send to {ctx.message.author.name}...")
        embed.set_thumbnail(url=ctx.message.server.icon_url)
        if ctx.message.author.id in self.donators:
            embed.set_footer(text="Your embed preview")
        else:
            embed.set_footer(text="This is what your bump message would look like if you were premium!")
        try:
            await self.bot.whisper(embed=embed)
            await self.bot.edit_message(a, "Sent to Dms.")
        except discord.Forbidden:
            await self.bot.edit_message(a, "Dming failed. sending to channel")
            await self.bot.say(embed=embed)


    @commands.command(pass_context=True, aliases=['ii', 'invinfo', 'invi'])
    async def inviteinfo(self, ctx, invite: discord.Invite = None, server: discord.Server.id = None):
        """Get invite information."""
        if server == None:
            server = self.bot.get_server(id=invite.server.id)
        else:
            server = self.bot.get_server(id=server)
        if invite == None:
            await self.bot.say("No invite detected.")
            return
        else:
            themsgtodel = await self.bot.say("gathering info...")
            invitec = await self.bot.invites_from(server)
            for inv in invitec:
                if inv != invite:
                    pass
                else:
                    if inv.max_age == 0:
                        ma = "infinite"
                    elif inv.max_age == 86400:
                        ma = '24h'
                    elif inv.max_age == 43200:
                        ma = '12h'
                    elif inv.max_age == 21600:
                        ma = '6h'
                    elif inv.max_age == 3600:
                        ma = '1h'
                    else:
                        ma = inv.max_age
                    if inv.max_uses == 0:
                        mu = "unlimited"
                    else:
                        mu = inv.max_uses
                    url = inv.url
                    code = inv.id
                    invi = inv.inviter.mention
                    if inv.uses == 0:
                        use = "Never used!"
                    else:
                        use = inv.uses
                    channel = inv.channel.mention




            e = discord.Embed(title=f"Info:", description=f"**Max age**: {ma}\n**Max uses**: {mu}\n**Url**: {url}\n"
                                                          f"**Code**: {code}\n**Created by**: {invi}\n**Server**: {inv.server.name}\n**Uses**: {use}\n"
            f"**For**: {channel}",color=randint(0, 0xffffff))
            e.set_thumbnail(url=inv.server.icon_url)
            await self.bot.say(embed=e)
            await self.bot.delete_message(themsgtodel)

    @commands.command(pass_context=True, aliases = ['li', 'invlist'])
    async def listinvites(self, ctx, serverid: int = None):
        """List a/current server's invites."""
        start = time.time()
        sid = serverid
        if sid == None:
            sid = ctx.message.server.id
            sserver = self.bot.get_server(id=sid)
        else:
            sserver = self.bot.get_server(id=sid)
        urls = ""
        m = await self.bot.invites_from(sserver)
        for i in m:
            if i.max_uses == 0:
                mu = 'Unlimited'
            else:
                mu = i.max_uses
            if i.max_age == 0:
                ma = 'Infinite'
            else:
                ma = i.max_age

            urls += f"**{i.url}** | Max Age: {ma} | Max Uses: {mu}\n"

        codes = ""
        for i in m:
            if i.max_uses == 0:
                mu = 'Unlimited'
            else:
                mu = i.max_uses
            if i.max_age == 0:
                ma = 'Infinite'
            else:
                ma = i.max_age
            codes += f"**{i.id}** | Max Age: {ma} | Max Uses: {mu}\n"
        end = time.time()
        e = discord.Embed(title=f"{sserver.name}'s invites:", description="below are invites.", color=randint(0, 0xffffff))
        e.add_field(name="Codes:", value=codes, inline=False)
        e.add_field(name="Urls:", value=urls, inline=False)
        e.set_footer(icon_url=sserver.icon_url, text=f"Retrieved in {round(end - start)} seconds (rounded). • you can do"
        f" -ii <code> on any of the above.")
        try:
            await self.bot.say(embed=e)
        except discord.HTTPException as e:
            e = discord.Embed(title=f"{sserver.name}'s invites:", description="below are invites.", color=randint(0, 0xffffff))
            e.add_field(name="HTTPException", value="Either the embed was too long (too many invites), or"
                                                    " some internal error occured, preventing the embed from being sent."
                                                    " For this reason, if you reply `continue` only codes will be displayed.")
            await self.bot.say(embed=e)
            confirmation = await self.bot.wait_for_message(author=ctx.message.author, channel = ctx.message.channel, timeout=60)
            if confirmation.content is None:
                return
            elif confirmation.content == 'continue':
                for p in pagify(codes):
                    await self.bot.say(p)
                    return
            else:
                await self.bot.say("Invalid response - quitting...")

    @commands.command(pass_context=True)
    async def invites(self, ctx, member: discord.User = None):
        """Get invites from user"""
        server = ctx.message.server
        if member == None:
            member = ctx.message.author
        else:
            member = member
        invitestotal = 0
        invites = await self.bot.invites_from(server)
        for i in invites:
            if i.inviter.id == member.id:
                invitestotal += int(invitestotal) + i.uses
            else:
                pass
        e = discord.Embed(title=f"{member.name}'s info:", description=invitestotal, color=0x000333)
        e.set_footer(text="Doesnt check if the same user joined via the invite, just adds all `uses` up")
        await self.bot.say(embed=e)

    @commands.command(pass_context=True)
    async def length(self,ctx, characters: str):
        """Check the amount of chars that is provided."""
        l = len(characters)
        if l >= 1600:
            await self.bot.say("Looks like your input was greater then 1600 chars. due to limitations, you can only send"
                               "1992 characters. would you like to send more/multiple 2k chars? [y/n]")
            q = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
            if q.content == 'n':
                await self.bot.say(f"Ok. here was your length: {l}")
                return
            elif q.content == 'y':
                await self.bot.say("Please input paragraph(s). say `quit` to exit.")
                characters = ""
                while True:
                    p = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
                    if p.content == 'quit':
                        await self.bot.say(f"Your total length: {len(characters)}")
                        return
                    else:
                        characters += str(p.content)
                        await self.bot.delete_message(p)
            else:
                await self.bot.say("invalid input")
        else:
            await self.bot.say(f"Character length: {l}")



        await self.bot.say(f"Input length: {l}")

    @commands.command(aliases=['bav', 'av', 'bigav', 'bigavatar'])
    async def bavatar(self, user: discord.Member):
        """Get a large avatar image"""
        e = discord.Embed(color=user.color, timestamp=datetime.datetime.now())
        if user.avatar == None:
            e.set_image(url=user.default_avatar_url)
            e.set_author(url=user.default_avatar_url, name=user.name)
            e.set_footer(text="Not displaying? well fyi its a default avatar, nothin special.")
        else:
            e.set_image(url=user.avatar_url)
            e.set_author(url=user.avatar_url, name=user.name)
            e.set_footer(text="Not displaying? click the author name")
        await self.bot.say(embed=e)


    @commands.command(pass_context=True)
    async def premcheck(self,ctx,  userid: str = None):
        """check premium user & names"""
        if userid == None:
            em = discord.Embed(title="Displaying Premium users and their names", color=0xfac905)
            for user in self.donators:
                m = await self.bot.get_user_info(user)
                em.add_field(name=m.name, value=m.id)
            await self.bot.say(embed=em)
            return
        else:
            for inte in self.donators:
                if inte == userid:
                    await self.bot.say("True")
                    return
            await self.bot.say("False")

    @commands.command(pass_context=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def roleinfo(self, role: str = None):
        """Get role(s) info"""
        if role is None:
            await self.bot.say("You need to say a role! accepted ways: `role ID`/`role name`/`role mention`")

def setup(bot):
    n = CoreCommands(bot)
    bot.remove_command('help')
    bot.add_cog(n)
