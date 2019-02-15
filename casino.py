import discord, asyncio, random, json
from discord.ext import commands

class Casino:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rr'])
    async def roulette(self, color: str):
        """
        Play a game of rr!
        usage: -rr <red/black>
        """
        colors = random.choice(['Red', 'red', 'black', 'Black'])
        embed=discord.Embed(title="Betting! Awaiting winning color...", description="Red | Black", color=0xffaa99)
        if colors == 'Black':
            w = discord.Embed(title="And the winning color is...", description="~~Red~~ | Black", color=0x000000)
        else:
            w = discord.Embed(title="And the winning color is...", description="Red | ~~Black~~", color=0xe93333)

        if color == colors:
            w.add_field(name="You win!", value="roll again?")
        elif color != colors:
            w.add_field(name="You lost.",value="better luck next time")
        else:
            await self.bot.say("Unknown error")


        try:
            msg = await self.bot.say(embed=embed)
            await asyncio.sleep(2)
        except discord.Forbidden:
            await self.bot.say("Error 403: discord.Forbidden\nI may not have the required permissions. I require"
                               " for this command the `embed-links` permission. this is also `a` required permission (-mperms).")
            await self.bot.say(f"Winning color: {colors}")
        await self.bot.edit_message(msg, embed=w)

    @commands.command(aliases=['slots'])
    async def slotmachine(self, info: str = None):
        """Roll a slot!"""
        if info == None:
            pass



def setup(bot):
    bot.add_cog(Casino(bot))
