from discord.ext import commands
import discord.utils


def is_owner_check(message):
    return message.author.id in ["421698654189912064", "269340844438454272", "493790026115579905"]


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def mod_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Mod', "Moderator", 'Admin', 'Administrator'), **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name in ('Admin', 'Administrator'), **perms)

    return commands.check(predicate)


def serverowner_or_permissions(**perms):
    def predicate(ctx):
        if ctx.message.server is None:
            return False
        server = ctx.message.server
        owner = server.owner

        if ctx.message.author.id == owner.id:
            return True

        return check_permissions(ctx,perms)
    return commands.check(predicate)

def serverowner():
    return serverowner_or_permissions()


def globaladmin():
    admins = ["421698654189912064", "269340844438454272", "493790026115579905"]
    def predicate(ctx):
        if ctx.message.author.id in admins:
            return True
    return commands.check(predicate)


def premcheck():
    donators = ['421698654189912064', '415912795574501386', '344878404991975427', '269340844438454272',
                     '293066151695482882', '493790026115579905', '365659613821009920']
    def predicate(ctx):
        if ctx.message.author.id in donators:
            return True
        return commands.check(predicate)