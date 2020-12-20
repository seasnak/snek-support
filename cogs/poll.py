from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, question, *reactions):
        poll = await ctx.channel.send(f"{question}")
        for reaction in reactions:
            await poll.add_reaction(reaction)
        await ctx.message.delete()
        return

def setup(bot):
    bot.add_cog(Poll(bot))

def teardown(bot):
    bot.remove_cog(Poll(bot))
