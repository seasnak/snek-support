from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, message):
        await message.channel.send(f"Hello {message.author.mention}")
        return

def setup(bot):
    bot.add_cog(Hello(bot))

def teardown(bot):
    bot.remove_cog(Hello(bot))
