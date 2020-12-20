from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, question):
        poll = await ctx.channel.send(f"{ctx.message.content}")
        return

def setup(bot):
    bot.add_cog(Poll(bot))

def teardown(bot):
    bot.remove_cog(Poll(bot))
