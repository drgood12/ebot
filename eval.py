import io
import textwrap
import traceback
import time
from contextlib import redirect_stdout

from discord.ext import commands


class Eval:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    @staticmethod
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # Remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

    @commands.command(pass_context=True, hidden=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        if str(ctx.message.author.id) in ["421698654189912064", "269340844438454272"]:
            
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.message.channel,
                'author': ctx.message.author,
                'server': ctx.message.server,
                'message': ctx.message,
                '_': self._last_result
            }

            env.update(globals())

            body = self.cleanup_code(self, body)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await self.bot.say(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            before = time.monotonic()
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await self.bot.say(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await self.bot.add_reaction('\u2705')
                except Exception as e:
                    pass

                if ret is None:
                    if value:
                        await self.bot.say(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await self.bot.say(f'```py\n{value}{ret}\n```')
            ping = round(time.monotonic() - before)
            p = time.monotonic() - before
            await self.bot.say(f"Success! `{ping}`s\nExact time: `{p}`s")
        else:
            await self.bot.say("Nosey noobs always tryina' get into private commands -_-")


def setup(bot):
    bot.add_cog(Eval(bot))
