import discord
from discord.ext import commands
from random import randint
from cogs.utils import checks
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='mod.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class General:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def perms(self, ctx, user: discord.Member = None, channel: discord.Channel = None):
        """Fetch a specific user's permissions."""
        if user is None:
            user = ctx.message.author
        if channel is None:
            channel = ctx.message.channel

        perms = iter(channel.permissions_for(user))
        perms_we_have = "```diff\n"
        perms_we_dont = ""
        for x in perms:
            if "True" in str(x):
                perms_we_have += "+ {0}\n".format(str(x).split("'")[1])
            else:
                perms_we_dont += "- {0}\n".format(str(x).split("'")[1])
        try:
            embed = discord.Embed(title="_ _",
                                  description="{0}{1}```".format(perms_we_have, perms_we_dont),
                                  color=0xfac905)
            await self.bot.say("{0}{1}```".format(perms_we_have, perms_we_dont))
        except Exception as e:
            await self.bot.whisper(f"The bot was prevented from sending in the channel because: `{e}`. "
                                   f"if `send_messages` is red, this is why. "
                                   f"please contact an admin to give me that perm. Let them also know that the bot does"
                                   f"not have it's minimum perms, which is bannable from TOS.")

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str):
        """mute x member
        """
        dude = member
        to = discord.Object(id=541361039271526400)
        server = discord.Server
        ci = randint(1, 9999)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        try:
            role = discord.utils.get(ctx.message.server.roles, name='Muted')
            if role is None:
                await self.bot.create_role(ctx.message.server, name='Muted')
                await self.bot.say("Muted role created; applying now")
            channels = ctx.message.server.channels
            role = discord.utils.get(ctx.message.server.roles, name='Muted')
            await self.bot.add_roles(member, role)
            for channel in ctx.message.server.channels:
                await self.bot.edit_channel_permissions(channel, role, overwrite)
            await self.bot.say("Muted {}. your case ID: {} (use -h caseid for info on case IDs)".format(member, ci))
            embed = discord.Embed(title=f"Mute command executed in {ctx.message.server.name}:",
                                  description="server ID: {}".format(ctx.message.server.id),
                                  color=randint(0, 0xffffff))
            embed.add_field(name="Moderator:", value="{} ({})".format(ctx.message.author.name, ctx.message.author.id))
            embed.add_field(name="Muted member:", value="{} ({})".format(dude, dude.id), inline=False)
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text="Case ID: {}".format(ci))
            await self.bot.send_message(to, embed=embed)
            await self.bot.send_message(dude,
                                        "You were Muted from {} by `{}{}` with reason: `{}`.".format(
                                            ctx.message.server.name,
                                            ctx.message.author.name,
                                            ctx.message.author.discriminator,
                                            reason)
                                        )
            await self.bot.say("Muted with reason: `{}`. Your case ID: {}".format(reason, ci))
        except Exception as e:
            raise e

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str):
        """Unmute x member"""
        to = discord.Object(id=541361039271526400)
        server = discord.Server
        ci = randint(1, 9999)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = True
        dude = member
        try:
            role = discord.utils.get(ctx.message.server.roles, name='Muted')
            if role is None:
                await self.bot.say("Muted role not found. This means the user *shouldn't* be muted.")
            channels = ctx.message.server.channels
            role = discord.utils.get(ctx.message.server.roles, name='Muted')
            await self.bot.remove_roles(member, role)
            await self.bot.say("Unmuted {}. your case ID: {} (use -h caseid for info on case IDs)".format(member, ci))
            embed = discord.Embed(title=f"unmute command executed in {ctx.message.server.name}:",
                                  description="server ID: {}".format(ctx.message.server.id), color=randint(0, 0xffffff))
            embed.add_field(name="Moderator:", value="{} ({})".format(ctx.message.author.name, ctx.message.author.id))
            embed.add_field(name="unMuted member:", value="{} ({})".format(dude, dude.id), inline=False)
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text="Case ID: {}".format(ci))
            await self.bot.send_message(to, embed=embed)
            await self.bot.send_message(dude, "You were Unmuted from {} by `{}{}` with reason: `{}`.".format(
                ctx.message.server.name, ctx.message.author.name,
                ctx.message.author.discriminator, reason))
            await self.bot.say("Unmuted with reason: `{}`. Your case ID: {}".format(reason, ci))
        except Exception as e:
            raise e

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, dude: discord.Member, *, reason: str):
        """Kick x member for y reason"""
        to = discord.Object(id=541361039271526400)
        server = discord.Server
        CI = randint(1, 9999)
        try:
            await self.bot.kick(dude)
            embed = discord.Embed(title=f"Kick command executed in {ctx.message.server.name}:",
                                  description="server ID: {}".format(ctx.message.server.id), color=randint(0, 0xffffff))
            embed.add_field(name="Moderator:", value="{} ({})".format(ctx.message.author.name, ctx.message.author.id))
            embed.add_field(name="Kicked member:", value="{} ({})".format(dude, dude.id), inline=False)
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text="Case ID: {}".format(CI))
            await self.bot.send_message(to, embed=embed)
            await self.bot.send_message(dude, "You were kicked from {} by `{}{}` with reason: `{}`.".format(
                ctx.message.server.name, ctx.message.author.name, ctx.message.author.discriminator, reason))
            await self.bot.say("Kicked {}. your case ID: {} (use -h caseid for info on case IDs)".format(dude, CI))

        except Exception as e:
            await self.bot.say(f"error:\n```py\n{e}\n```")
            await self.bot.kick(dude)
            embed.add_field(name="Error:", value=f"```py\n{e}\n```")
            await self.bot.send_message(to, embed=embed)


    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, dude: discord.Member, *, reason: str):
        """Ban x for y reason"""
        to = discord.Object(id=541361039271526400)
        server = discord.Server
        CI = randint(1, 9999)
        try:
            await self.bot.ban(dude)
            embed = discord.Embed(title=f"Ban command executed in {ctx.message.server.name}:",
                                  description="server ID: {}".format(ctx.message.server.id), color=randint(0, 0xffffff))
            embed.add_field(name="Moderator:", value="{} ({})".format(ctx.message.author.name, ctx.message.author.id))
            embed.add_field(name="Banned member:", value="{} ({})".format(dude, dude.id))
            embed.add_field(name="Reason", value=reason)
            embed.set_footer(text="Case ID: {}".format(CI))
            await self.bot.send_message(to, embed=embed)
            await self.bot.send_message(dude, "You were Banned from {} by `{}{}` with reason: `{}`.".format(
                ctx.message.server.name, ctx.message.author.name, ctx.message.author.discriminator, reason))
            await self.bot.say("Banned {}. your case ID: {} (use -h caseid for info on case IDs)".format(dude, CI))

        except Exception as e:
            await self.bot.say(f"an error occured:\n```py\n{e}\n```")
            embed.add_field(name="Error:", value=f"```py\n{e}\n```")
            await self.bot.send_message(to, embed=embed)

    @commands.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def hackban(self, ctx, user_id: int, *, reason: str = None):
        """Preemptively bans user from the server

        A user ID needs to be provided
        If the user is present in the server a normal ban will be
        issued instead"""
        user_id = str(user_id)
        author = ctx.message.author
        server = author.server

        ban_list = await self.bot.get_bans(server)
        is_banned = discord.utils.get(ban_list, id=user_id)

        if is_banned:
            await self.bot.say("already banned skrub")
            return

        user = server.get_member(user_id)
        if user is not None:
            await ctx.invoke(self.ban, user=user, reason=reason)
            return

        try:
            await self.bot.http.ban(user_id, server.id, 0)
            e = discord.Embed(title="Hackban")
            await self.bot.say("Success.")
        except discord.NotFound:
            await self.bot.say("User not found. Have you provided the "
                               "correct user ID?")
        except discord.Forbidden:
            await self.bot.say("I lack the permissions to do this.")

    @commands.command(pass_context=True)
    @checks.admin_or_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, userid: int):
        """unban x"""
        u = await self.bot.get_user_info(userid)
        await self.bot.unban(c)

def setup(bot):
    bot.add_cog(General(bot))