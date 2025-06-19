from discord.ext import commands

import config
import re
import random

MAX_AMOUNT: int = 100
MIN_AMOUNT: int = 1

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    async def adjust_credit(self, context: commands.Context, target:str, amount):
        target_match: re.Match|None = re.match(r"<@!?(\d+)>", target)
        if target_match == None:
            await context.channel.send(f"Could not find user.")
            return
        target_id = int(target_match.group(1))
        if target_id == context.author.id:
            return

        await context.message.add_reaction("👍")
        if target_id not in config.user_social_credit:
            config.user_social_credit[target_id] = 1000
        config.user_social_credit[target_id] += amount

        return

    @commands.hybrid_command(
        name="toxicity",
        desc="Report a toxic individual."
    )
    async def toxicity(self, context: commands.Context, target: str):
        amount = random.randint(1, 100)
        await self.adjust_credit(context, target, -amount)
        return

    @commands.hybrid_command(
        name="generosity",
        desc="Support a positive individual."
    )
    async def generosity(self, context: commands.Context, target: str):
        amount = random.randint(1, 100)
        await self.adjust_credit(context, target, amount)
        return

    @commands.hybrid_command(
        name="standings",
        desc="Lists all individuals and their social credit scores."
    )
    async def standings(self, context: commands.Context):
        message: str = ""
        config.user_social_credit = dict(sorted(config.user_social_credit.items()))

        for i, user_id in enumerate(config.user_social_credit.keys()):
            user = await context.bot.fetch_user(user_id)
            social_credit = config.user_social_credit[user_id]
            message += f"{i+1}. {user.name}: {social_credit}\n"
            # print(user, " ", social_credit)
        await context.channel.send(message)
        return
    
    @commands.hybrid_command(
        name="credit",
        desc="Returns your current Social Credit score.",
    )
    async def credit(self, context: commands.Context):
        user_id: int = context.author.id
        await context.channel.send(f"{context.author.mention}\'s social credit: {config.user_social_credit.get(user_id)}")
        return

async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.add_cog(SocialCredit(bot))
    return 
