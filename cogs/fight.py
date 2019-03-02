
# probably such a big file it would be pointless putting it in main.py.
import discord, asyncio
from discord.ext import commands
from random import randint

class Fight:

    def __init__(self, bot):
        self.bot = bot
# default sh*t
default_health = 0
weapons = {'Blunt sword': 3,
           'Sharp sword': 4,
           'god\'s sword': 20,
           'primitive bow': 1,
           'modern bow': 6,
           'Hunting bow': 10,
           'standard pistol': 4,
           'silent pistol': 2,
           'SMP': 20,
           'javascript': 90,
           '360 noscope': 60,
           'bat': 8}



    @commands.command(pass_context=True)
    async def fight(self, user: discord.User):
        """Take out your rage on someone else. or endure more via a defeat."""

