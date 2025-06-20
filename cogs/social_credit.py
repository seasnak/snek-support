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

    def find_user_id(self, username: str) -> int:
        # Returns the usernameID given the user mention.
        match_username: re.Match|None = re.match(r"<@!?(\d+)>", username)
        return -1 if match_username == None else int(match_username.group(1))

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

        username= await context.bot.fetch_user(target_id)
        new_credit = max(0, config.user_social_credit[target_id] + amount)
        if target_id not in config.user_social_credit:
            config.user_social_credit[target_id] = 1000
        try:
            await context.message.add_reaction("👍")
        # except NotFound:
        #     print("Message not found")
        except Exception as exception:
            print(f"Error adjusting credit for username{target_id}. {type(exception).__name__}.") 
        await context.send(f"{username}: {config.user_social_credit[target_id]} [{"+" if amount > 0 else ""}{amount}] = {new_credit}")
        config.user_social_credit[target_id] = new_credit
        
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
    async def standings(self, context: commands.Context, resort=True):
        message: str = ""
        if resort:
            config.user_social_credit = {k: v for k,v in sorted(config.user_social_credit.items(), key=lambda item: item[1], reverse=True)}

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
    async def credit(self, context: commands.Context, username: str = "self"):
        user_id: int = context.author.id if username== "self" else self.find_user_id(username)
        if user_id < 0:
            await context.send(f"usernamenot found.")
            return

        if user_id not in config.user_social_credit.keys():
            config.user_social_credit[user_id] = 1000

        await context.send(f"{context.author.mention}\'s social credit: {config.user_social_credit.get(user_id)}")
        return
    
    @commands.hybrid_command(
        name="removeuser",
        desc="Removes a usernamefrom the Social Credit System", 
    )
    @commands.is_owner()
    async def removeuser(self, context: commands.Context, username: str):
        user_id = self.find_user_id(username)
        try:
            config.user_social_credit.pop(user_id)
            await context.send(f"Removed {username}.")
        except:
            await context.send("Failed to remove user.")
        return

async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.add_cog(SocialCredit(bot))
    return 
