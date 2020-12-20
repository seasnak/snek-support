from discord.ext import commands
import random

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @commands.command()
    async def anime(self, ctx):
        print("Anime command called")
        return

def setup(bot):
    bot.add_cog(Anime(bot))
