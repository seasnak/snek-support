from discord.ext import commands

import config

class Crocoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return
    
    @commands.hybrid_command(
        name="crocoins",
        description:"Get the number of crocoins you have"
    )
    async def crocoins(self, context: commands.Context, user: str):
        




async def setup(bot):
    await bot.add_cog(Crocoins(bot))

async def teardown(bot):
    await bot.remove_cog(Crocoins(bot))
