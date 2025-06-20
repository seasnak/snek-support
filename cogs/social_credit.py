from discord import NotFound
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

    def find_user_id(self, user: str) -> int:
        # Returns the User ID given the user mention.
        match_user: re.Match|None = re.match(r"<@!?(\d+)>", user)
        return -1 if match_user == None else int(match_user.group(1))

    async def adjust_credit(self, context: commands.Context, target:str, amount):
        target_id = self.find_user_id(target)
        if target_id < 0: return
        await self.adjust_id_credit(context, target_id, amount)
        return

    async def adjust_id_credit(self, context:commands.Context, target_id:int, amount: int):        
        if target_id == context.author.id:
            try:
                await context.message.add_reaction("👎")
            except NotFound:
                await context.send("...")
            except Exception as exception:
                print(f"{type(exception).__name__} Error: {exception}.")
            return

        user = await context.bot.fetch_user(target_id)
        
        if target_id not in config.user_social_credit:
            config.user_social_credit[target_id] = 1000
        try:
            await context.message.add_reaction("👍")
        except NotFound:
            await context.send(f"Success on {user}: {config.user_social_credit[target_id]}[{"+" if amount > 0 else ""}{amount}]")
        except Exception as exception:
            print(f"Error adjusting credit for user {target_id}. {type(exception).__name__}.") 
        config.user_social_credit[target_id] = max(0, config.user_social_credit[target_id] + amount)

        return

    @commands.hybrid_command(
        name="toxicity",
        description="Report a toxic individual."
    )
    async def toxicity(self, context: commands.Context, target: str):
        amount = random.randint(1, 100)
        await self.adjust_credit(context, target, -amount)
        return

    @commands.hybrid_command(
        name="generosity",
        description="Support a positive individual."
    )
    async def generosity(self, context: commands.Context, target: str):
        amount = random.randint(1, 100)
        await self.adjust_credit(context, target, amount)
        return

    @commands.hybrid_command(
        name="standings",
        description="Lists all individuals and their social credit scores."
    )
    async def standings(self, context: commands.Context):
        message: str = ""
        config.user_social_credit = dict(sorted(config.user_social_credit.items(), key=lambda item: item[1], reverse=True))

        for i, user_id in enumerate(config.user_social_credit.keys()):
            user = await context.bot.fetch_user(user_id)
            social_credit = config.user_social_credit[user_id]
            message += f"{i+1}. {user.name}: {social_credit}\n"
        await context.send(message)
        return

    @commands.hybrid_command(
        name="credit",
        description="Returns your current Social Credit score.",
    )
    async def credit(self, context: commands.Context, user: str = "self"):
        user_id: int = context.author.id if user == "self" else self.find_user_id(user)
        if user_id < 0:
            await context.send(f"User not found.")
            return

        if user_id not in config.user_social_credit.keys():
            config.user_social_credit[user_id] = 1000

        await context.send(f"{context.author.mention}\'s social credit: {config.user_social_credit.get(user_id)}")
        return

async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.add_cog(SocialCredit(bot))
    return 
