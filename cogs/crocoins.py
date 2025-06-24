from discord.ext import commands

import config
from datetime import datetime

class Crocoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return
    
    @commands.hybrid_command(
        name="crocoins",
        description="Get the number of crocoins you have",
    )
    async def crocoins(self, context: commands.Context, user: str): 
        
        return 
    
    @commands.hybrid_command(
        name="gamble",
        description="Gamble a certain amount of coins!"
    )
    async def gamble(self, context: commands.Context, wager: int = -1):
        user_id = context.author.id
        user = config.users[user_id]
        if wager == -1:
            wager = user.crocoins
        
        return

async def setup(bot):
    await bot.add_cog(Crocoins(bot))

async def teardown(bot):
    await bot.remove_cog(Crocoins(bot))
