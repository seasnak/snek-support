from discord import NotFound
from discord.ext import commands

import time
from datetime import datetime

import config
import random
import utils
import math

import pickle

MAX_AMOUNT: int = 100
MIN_AMOUNT: int = 1

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def adjust_credit(self, context: commands.Context, target:str, amount):
        target_id = utils.find_user_id(target)
        if target_id < 0: return
        await self.adjust_id_credit(context, target_id, amount)
        return

    async def adjust_id_credit(self, context:commands.Context, target_id:int, amount: int, allow_self: bool = False): 
        if target_id == context.author.id and allow_self == False:
            try:
                await context.message.add_reaction("👎")
            except NotFound:
                await context.send("...")
            except Exception as exception:
                print(f"{type(exception).__name__} Error: {exception}.")
            return

        username= await context.bot.fetch_user(target_id)
        if target_id not in config.user_social_credit:
            config.user_social_credit[target_id] = 1000
        
        start_credit = config.user_social_credit[target_id]
        new_credit = max(-1000, start_credit + amount)
        try:
            await context.message.add_reaction("👍")
        # except NotFound:
        #     print("Message not found")
        except Exception as exception:
            print(f"Error adjusting credit for username{target_id}. {type(exception).__name__}.") 
        await context.send(f"{username}: {start_credit} [{"+" if amount > 0 else ""}{amount}] = {new_credit}")
        config.user_social_credit[target_id] = new_credit
        
        return

    @commands.hybrid_command(
        name="toxicity",
        description="Report a toxic individual."
    )
    async def toxicity(self, context: commands.Context, target: str):
        author_id = context.author.id
        TOXICITY_COOLDOWN = 30
        
        current_time = time.time()
        if author_id not in config.user_toxicity_timer:
            config.user_toxicity_timer[author_id] = current_time
        elif current_time - config.user_toxicity_timer[author_id] < TOXICITY_COOLDOWN:
            time_difference = int(current_time - config.user_toxicity_timer[author_id])
            await utils.send_context_message(context, f"Can't use that command yet! Wait {TOXICITY_COOLDOWN - time_difference} seconds and try again.")
            return
        
        config.user_toxicity_timer[author_id] = current_time
        amount = random.randint(1, 100)
        
        if "random" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            await self.adjust_id_credit(context, random_target, -amount, allow_self=True)
        else:
            await self.adjust_credit(context, target, -amount)
        return

    @commands.hybrid_command(
        name="generosity",
        description="Support a positive individual."
    )
    async def generosity(self, context: commands.Context, target: str):
        amount = random.randint(1, 100)

        if "random" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            await self.adjust_id_credit(context, random_target, amount, allow_self=True)
        else:
            await self.adjust_credit(context, target, amount)
        return

    @commands.hybrid_command(
        name="standings",
        description="Lists all individuals and their social credit scores."
    )
    async def standings(self, context: commands.Context, resort=True, save=False):
        message: str = ""
        if resort:
            config.user_social_credit = {k: v for k,v in sorted(config.user_social_credit.items(), key=lambda item: item[1], reverse=True)}

        for i, user_id in enumerate(config.user_social_credit.keys()):
            user = await context.bot.fetch_user(user_id)
            social_credit = config.user_social_credit[user_id]
            message += f"{i+1}. {user.name}: {social_credit}\n"

        try:
            await context.send(message)
        except:
            await context.channel.send(message)

        if save == True:
            await self.save_social_credit(context)
        return

    @commands.hybrid_command(
        name="credit",
        description="Returns your current Social Credit score.",
    )
    async def credit(self, context: commands.Context, username: str = "self"):
        user_id: int = context.author.id if username== "self" else utils.find_user_id(username)
        if user_id < 0:
            await context.send(f"User not found.")
            return

        if user_id not in config.user_social_credit.keys():
            config.user_social_credit[user_id] = 1000
        
        user = await context.bot.fetch_user(user_id)
        await context.send(f"{user.name}\'s social credit: {config.user_social_credit.get(user_id)}")
        return
    
    @commands.hybrid_command(
        name="removeuser",
        description="Removes a username from the Social Credit System", 
    )
    @commands.is_owner()
    async def removeuser(self, context: commands.Context, username: str):
        user_id = utils.find_user_id(username)
        if user_id < 0: 
            await context.send("User not found.")
            return
        
        user = await context.bot.fetch_user(user_id)
        try:
            config.user_social_credit.pop(user)
            await context.send(f"Removed {user.name}.")
        except:
            await context.send("Failed to remove user.")
        return

    @commands.hybrid_command(
        name="adduser",
        description="Adds a user to the social credit. "
    )
    @commands.is_owner()
    async def adduser(self, context: commands.Context, username: str, start_amount: int = 1000): 
        user_id = utils.find_user_id(username)
        if user_id < 0: 
            await context.send("User not found.")
            return
        
        user = await context.bot.fetch_user(user_id)
        config.user_social_credit[user_id] = start_amount
        await context.send(f"Added {user.name} with a credit of {start_amount}.")
        return

    @commands.hybrid_command(
        name="adjustcredit",
        description="Adjust credit for user. Use negative number for reductions"
    )
    @commands.is_owner()
    async def adjustcredit(self, context: commands.Context, username: str, adjustment: int):
        user_id = utils.find_user_id(username)
        if user_id < 0:
            await context.send("User not found.")
            return
        
        if user_id not in config.user_social_credit.keys():
            config.user_social_credit[user_id] = 1000

        user = await context.bot.fetch_user(user_id)
        config.user_social_credit[user_id] += adjustment
        await context.send(f"{user.name}: {"+" if adjustment>0 else ""}{adjustment} => {config.user_social_credit[user_id]}")
        return

    @commands.hybrid_command(
        name="savecredit",
        description=""
    )
    @commands.is_owner()
    async def save_social_credit(self, context: commands.Context, filename: str = 'socialcredit.pkl'):
        file = open(filename, 'wb')
        pickle.dump(config.user_social_credit, file)
        
        try:
            await context.send("Successfully saved user social credit.")
        except:
            await context.channel.send("Successfully saved user social credit.")
        return
    
    @commands.hybrid_command(
        name="loadcredit",
        description="",
    )
    @commands.is_owner()
    async def load_social_credit(self, context: commands.Context, filename: str = 'socialcredit.pkl'): 
        file = open(filename, 'rb')
        config.user_social_credit = pickle.load(file)

        try:
            await context.send("Succesfully loaded user social credit")
        except:
            await context.channel.send("Successfully loaded user social credit")
        return

async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.remove_cog(SocialCredit(bot))
    return 
