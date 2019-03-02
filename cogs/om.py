import discord, datetime
from discord.ext import commands
from .utils import checks

class Om:

    def __init__(self, bot):
        self.bot = bot
        self.to = '550739999541166081'



    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        author = message.author
        if isinstance(message.channel, discord.PrivateChannel):
            for server in self.bot.servers:
                member = server.get_member(author.id)
                if member:
                    author = member
                break  # this is checking for silly nicknames.

            if isinstance(author, discord.Member) and author.nick:
                author_name = '{0.nick} ({0})'.format(author)
            else:
                author_name = str(author)
            embed = discord.Embed(
                color=0xff0000,
                description=message.content
                )
            embed.set_author(
                name=(author_name),
                icon_url=author.avatar_url if author.avatar else author.default_avatar_url)
            embed.set_footer(text="User ID: {}".format(author.id))

            if message.attachments:
                attachment_urls = []
                for attachment in message.attachments:
                    attachment_urls.append('[{}]({})'.format(attachment['filename'], attachment['url']))
                attachment_msg = '\N{BULLET} ' + '\n\N{BULLET} s '.join(attachment_urls)
                embed.add_field(
                    name='Attachments',
                    value=attachment_msg,
                    inline=False
                    )
            mothership = await self.bot.send_message(discord.Object(id=548927512034541568), embed=embed)
            await self.bot.send_message(discord.Object(id=548927512034541568), "User ID: {}".format(author.id))
            await self.bot.send_message(author, "Modmail successfully sent!")


    @commands.command(pass_context=True)
    @checks.globaladmin()
    async def reply(self, ctx, user: int, message: str):
        """reply to someone via id."""
        author = ctx.message.author
        embed=discord.Embed(title="ModMail reply!", description=message, color=0xfac905, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=ctx.message.author.name, icon_url=author.avatar_url)
        await self.bot.send_message(discord.User(id=user), embed=embed)

    async def on_message_delete(self, message):
        server = self.bot.get_server(message.id)
        e = discord.Embed(title="Deleted message!", description=message.content, color=message.author.color(),
                          timestamp=message.timestamp)
        e.set_author(name=message.author.name)
        e.set_footer(name=f"{server.name} | {message.author.name} | {message.channel.name}")
        await self.bot.send_message(discord.Object(id=self.to), embed=e)

    async def on_message_edit(self, before, after):
        e = discord.Embed(title="edited message", description=f"{before.content} -> {after.content}",
                          color=before.author.color, timestamp=after.edited_timestamp)
        e.set_author(name=message.author.name)
        e.set_footer(name=f"{server.name} | {message.author.name} | {message.channel.name}")
        await self.bot.send_message(discord.Object(id=self.to), embed=e)


def setup(bot):
    bot.add_cog(Om(bot))

