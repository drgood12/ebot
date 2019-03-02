import discord
from discord.ext import commands
from cogs.EcoUtil import *


def owner(ctx):
    return ctx.message.author.id in ['421698654189912064', '269340844438454272']


class Eco:
    def __init__(self, bot):
        self.data = None
        self.bot = bot

    @commands.command(pass_context=True)
    async def eco(self, ctx, *, stuff):
        print(self.data)
        if len(stuff.split()) == 1 and stuff.split()[0] == "init" and owner(ctx):
            self.data = await getdata()
            await self.bot.say("I've initialized the Eco module by loading EcoData.json")
            print(self.data)
        elif len(stuff.split()) > 1 and stuff.split()[0] == "data" and owner(ctx):
            if stuff.split()[1] == "json.upload":
                with open("EcoData.json", "rb") as ecodata:
                    await self.bot.say("Finding it... and.. oh! Here it is!")
                    await self.bot.send_file(ctx.message.channel, ecodata)
        elif len(stuff.split()) == 3 and stuff.split()[0] == "player" and stuff.split()[1] == "create":
            if not (self.data is None):
                pass
            else:
                await self.bot.say(
                    "So it looks like the devs didn't initialize the economy module.. I'll notify them asap.")
                await self.bot.send_message(discord.Object('538441181562929172'),
                                            f"You forgot to initialize the economy module, and because of it, "
                                            f"{str(ctx.message.author)} is suffering.")


def setup(bot):
    bot.add_cog(Eco(bot))
