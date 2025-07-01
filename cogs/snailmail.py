from discord import NotFound
from discord.ext import commands

from cogs.social_credit import SocialCredit
import config
import random
import utils
import pickle
from enum import Enum

class SnailMailMethod(Enum):
    SLUGGISH=1,
    SLOW=2,


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
