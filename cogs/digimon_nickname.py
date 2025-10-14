from discord import NotFound, app_commands
import discord
from discord.ext import commands, tasks

import time
from datetime import datetime

import config
import random

list_of_digimon : list[str] = []
list_of_digimon_filepath : str = "data/digimon.txt"
default_target = ""

class DigimonNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pass

    @commands.hybrid_command(
        name="reroll_diginame",
        description="Reroll the nickname for target"
    )
    @commands.is_owner()
    async def reroll_diginame(self, context: commands.Context, target_id: str = default_target):
        return

async def setup(bot):
    await bot.add_cog(DigimonNickname(bot))
    pass

async def teardown(bot):
    await bot.remove_cog(DigimonNickname(bot))
    pass
