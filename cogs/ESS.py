# ESS exclusive
import discord, random, asyncio
from random import randint
from discord.ext import commands
from .utils import checks


class Ess:
    
    def __init__(self, bot):
        self.bot = bot
        self.cid = randint(0, 999)
        self.modlog = discord.Object(544221067934171155)


    @commands.command(pass_context=True)
    @commands.has_any_role('Helper', 'Mod', 'Admin', 'Sr admin', 'Developer')
    async def et(self, ctx):
        a = ctx.message.author
        msg = f"{a} {a.name} {a.id} {a.discriminator} {a.mention} {list(a.permissions_in(ctx.message.channel))} "
        f"{a.status} {a.game} {a.top_role.name}"
        await self.bot.say(msg)

    @commands.command(pass_context=True, name='e.warn')
    @commands.has_any_role('Helper', 'Mod', 'Admin', 'Sr admin', 'Developer')
    async def w(self, ctx, user: discord.Member, *, reason: str = None):
        """Warn @user for *reason*"""
        defaultwarn = 'You were warned in Ebot Hub, reason: none. Case id: {}'.format(self.cid)

        # getting the reason
        if reason == None:
            reason = defaultwarn
        else:
            reason = reason
        # preparing modlog embed
        web = discord.Embed(title="Warn", description="Details below", color=0x419b35)
        web.add_field(name="Moderator", value=ctx.message.author.name)
        web.add_field(name="User", value="{} ({})".format(user.name, user.id))
        web.add_field(name="Reason", value=reason, inline=False)

        # sending messages
        try:
            await self.bot.send_message(user, f"You were `warned` in Ebot hub with reason: `{reason}`")
            await self.bot.send_message(self.modlog, embed=web)
            omsg = await self.bot.say("Successfully warned {} <:success:522078924432343040>".format(user.name))
            await asyncio.sleep(10)
            await self.bot.delete_message(ctx.message)
            await self.bot.delete_message(omsg)
        except discord.HTTPException:
            msg = await self.bot.say("Unable to dm {}. They will be notified here once logging is complete".format(user.name))
            web.add_field(name="Error:", value="Forbidden (403): couldn't Dm user")
            await self.bot.send_message(self.modlog, embed=web)
            tmsg = await self.bot.say("Semi-successfully warned {} :warning:".format(user.name))
            await asyncio.sleep(7)
            await self.bot.delete_message(msg)
            await self.bot.delete_message(tmsg)
            await self.bot.delete_message(ctx.message)
            await self.bot.say(f"{user.mention} you were warned, but i couldn't DM you with the reason! "
                               f"Here is your case ID if you want the reason: {self.cid}")

    @commands.command(pass_context=True,aliases = ['clearwarn', 'unwarn'])
    @commands.has_any_role('Mod', 'Admin', 'Sr admin', 'Developer')
    async def delwarn(self,ctx, mid: int):
        """Delete/clear a warning. does not DM the user"""
        try:
            id = await self.bot.get_message(channel=discord.Object(id=544221067934171155), id=mid)
            await self.bot.say("Please tell me the user @mention or ID so i can DM them. if they are nolonger in the "
                               "server, just say `n/a`. Times out in 120s (2m)")
            m = await self.bot.wait_for_message(channel = ctx.message.channel, author = ctx.message.author, timeout=120)
            if m == None or 'n/a':
                await self.bot.say("canceled")
            else:
                try:
                    await self.bot.send_message(m.content, "You were unwarned in Ebot Hub.")
                    try:
                        await self.bot.delete_message(id)
                    except discord.NotFound:
                        await self.bot.say("msg id not found in server-logs.")
                except Exception as e:
                    await self.bot.say(f"error: ```py\n{e}\n```")
                    await self.bot.say("canceled.")
            await self.bot.say("Success.")
        except discord.NotFound:
            await self.bot.say("discord.NotFound - Message ID not found in server-logs. please try again.")

    @commands.command()
    @commands.has_any_role('Admin', 'Sr admin', 'Developer')
    async def addrole(self, user: discord.Member, role: str = 'Members'):
        """Add a a role to member"""
        x = discord.utils.get(ctx.message.server.roles, name=role)
        try:
            if user == ctx.message.author:
                await self.bot.say("You can't give yourself roles...")
            else:
                await self.bot.add_role(user, x)
                await self.bot.say("success")
        except discord.HTTPException:
            await self.bot.say("HTTPException - operation failed. try again.")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 65, commands.BucketType.user)
    @commands.has_any_role('Members')
    async def rate(self, ctx,  member: discord.Member, outof: int, *, reason: str):
        """rate a support team member!"""
        support_team = ['500592278629515265','293160675394715650','421698654189912064','269340844438454272',
                        '402267423010455562','344878404991975427','405191549190930453']  # list of IDs
        if ctx.message.server.id == '486910899756728320':
            loading = "<a:loading:551413963766890527>"
            msg = await self.bot.say(f"Checking database {loading}")
            if member.id not in support_team:
                names = "`"
                for u in support_team:
                    m = await self.bot.get_user_info(u)
                    names += f"{m.name} | "
                names += '`'
                await self.bot.edit_message(msg, f"<:fail:522076877075251201> can't rate a member that is'nt in support team!"
                                   f" if they are in the support team please let EEKIM10_YT know, as their ID hasnt been"
                                   f" added to the system yet. available to rate: {names}")
            elif member.id == ctx.message.author.id:
                await self.bot.edit_message(msg, "You cant rate yourself!")
            else:
                if outof >= 10:
                    outof = 10
                if outof <= 1:
                    outof = 1
                e=discord.Embed(title="Support review!", color=0xfac905)
                e.add_field(name="Support member:", value=member.display_name, inline=False)
                e.add_field(name="Reviewer:", value=f"{ctx.message.author.display_name} ({ctx.message.author.mention})", inline=False)
                e.add_field(name="Rating", value="{}/10".format(outof), inline=False)
                e.add_field(name="Reason:", value=reason, inline=False)
                e.set_thumbnail(url=member.avatar_url)
                await self.bot.send_message(discord.Object(id=546319890361876502), embed=e)
                await self.bot.edit_message(msg, "Success!")
        else:
            await self.bot.say("Error - support server only")








        



def setup(bot):
    bot.add_cog(Ess(bot))
