from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="hello",
        description="I'll say hello to you!"
    )
    async def hello(self, context: commands.Context):
        await context.send(f"Hello {context.author.mention}")
        return

async def setup(bot):
    await bot.add_cog(Hello(bot))

async def teardown(bot):
    await bot.remove_cog(Hello(bot))
