from discord import NotFound
from discord.ext import commands

from cogs.social_credit import SocialCredit
import config
import random
import utils
import pickle
from enum import Enum

from datetime import datetime

class SnailMailMethod(Enum):
    SLUGGISH=1, # 3 months to a year
    SLOW=2, # 30 days to 3 months
    STANDARD=3, # 14 to 30 days 
    PRIORITY=4, # 7 to 14 days
    EXPRESS=5, # 5 to 7 days
    pass

snailmailduration = {
    SnailMailMethod.SLUGGISH: (),
    SnailMailMethod.SLOW: (),
    SnailMailMethod.STANDARD: (),
    SnailMailMethod.PRIORITY: (),
    SnailMailMethod.EXPRESS: (),

}



class SnailMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.hybrid_command(
        name="snailmail",
        description="send a message to someone!"
    )
    async def snailmail(self, context: commands.Context, method: SnailMailMethod, recipient: str, message: str):
        
        return


async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.remove_cog(SocialCredit(bot))
    return
