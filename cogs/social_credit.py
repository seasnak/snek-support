import discord
from discord import NotFound, app_commands
from discord.ext import commands, tasks

import time
from datetime import datetime

import config
import random
import utils
import math
from enum import Enum

import pickle

MAX_AMOUNT: int = 100
MIN_AMOUNT: int = 1

TOXICITY_COOLDOWN: int = 30

command_queue = []

class Modifier(Enum):
    NONE=0
    RANDOM=1
    pass

class SocialCredit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.handle_command_queue.start()
        print("Started Command Queue Handler")
    
    async def adjust_credit(self, context: commands.Context, target:str, amount: int):
        target_id = utils.find_user_id(target)
        if target_id < 0: return
        await self.adjust_id_credit(context, target_id, amount)
        return

    async def adjust_id_credit(self, context, target_id: int, amount: int, allow_self: bool = False, send_message = True):
        is_interaction = type(context) is discord.interactions.Interaction
        author_id = context.user.id if is_interaction else context.author.id
            
        if target_id == author_id and allow_self == False:
            try:
                await context.message.add_reaction("👎")
            except NotFound:
                await context.send("...")
            except Exception as exception:
                print(f"{type(exception).__name__} Error: {exception}.")
            return "ERROR"

        username = await context.client.fetch_user(target_id) if is_interaction else await context.bot.fetch_user(target_id)
        if target_id not in config.user_social_credit:
            config.user_social_credit[target_id] = 1000
        
        start_credit = config.user_social_credit[target_id]
        # new_credit = max(-1000, start_credit + amount)
        new_credit = start_credit + amount
        try:
            await context.message.add_reaction("👍")
        except Exception as exception:
            print(f"Error adjusting credit for username{target_id}. {type(exception).__name__}.")
        if send_message:
            message = f"{username}: {start_credit} [{"+" if amount > 0 else ""}{amount}] = {new_credit}"
            try:
                await context.send(message)
            except:
                await context.response.send_message(message)
        config.user_social_credit[target_id] = new_credit
        
        return f"{username}: {start_credit} [{"+" if amount > 0 else ""}{amount}] = {new_credit}"
    
    @commands.hybrid_command(
        name="equality",
        description="When will you learn..."
    )
    async def equality(self, context: commands.Context, target: str = "random"):
        author_id = context.author.id

        current_time = time.time()
        if author_id not in config.user_toxicity_timer:
            config.user_toxicity_timer[author_id] = current_time
        elif current_time - config.user_toxicity_timer[author_id] < TOXICITY_COOLDOWN:
            time_difference = int(current_time - config.user_toxicity_timer[author_id])
            await utils.send_context_message(context, f"Can't use that command yet! Wait {TOXICITY_COOLDOWN - time_difference} seconds and try again.")
            return
        
        config.user_toxicity_timer[author_id] = current_time
        amount = random.randint(1, 100)
        
        members = [member.id for member in context.guild.members]
        if "rand" in target.lower():
            random_toxicity_target_id = members[random.randint(0, len(members)-1)]
            random_generosity_target_id = members[random.randint(0, len(members)-1)]

            command_queue.append(('equality', context, (random_toxicity_target_id, random_generosity_target_id, amount)))
            return
        
        random_target_id = members[random.randint(0, len(members)-1)]
        target_id = utils.find_user_id(target)
        if target_id < 0: return
        target_is_generosity: bool = random.randint(0, 1) == 0
        
        if target_is_generosity:
            command_queue.append(('equality', context, (random_target_id, target_id, amount) ))
        else:
            command_queue.append(('equality', context, (target_id, random_target_id, amount) ))
        return
    
    
    @commands.hybrid_command(
        name="apology",
        description="Apologize to an individual",
    )
    async def apology(self, context: commands.Context, target: str = "random"):
        author_id = context.author.id
        amount = random.randint(1, 100)
        
        if "rand" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            # await self.adjust_id_credit(context, random_target, -amount, allow_self=True)
            command_queue.append(("equality", context, (author_id, random_target, amount)))
        else:
            # await self.adjust_credit(context, target, -amount)
            target_id = utils.find_user_id(target)
            command_queue.append(("equality", context, (author_id, target_id, amount)))
        return


    @commands.command(
        name="toxicity",
        description="Report a toxic individual."
    )
    async def toxicity_text(self, context: commands.Context, target: str = "random", *additional_targets):
        author_id = context.author.id
        
        current_time = time.time()
        if author_id not in config.user_toxicity_timer:
            config.user_toxicity_timer[author_id] = current_time
        elif current_time - config.user_toxicity_timer[author_id] < TOXICITY_COOLDOWN:
            time_difference = int(current_time - config.user_toxicity_timer[author_id])
            await utils.send_context_message(context, f"Can't use that command yet! Wait {TOXICITY_COOLDOWN - time_difference} seconds and try again.")
            return
        
        config.user_toxicity_timer[author_id] = current_time
        amount = random.randint(1, 100)
        
        if "rand" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            # await self.adjust_id_credit(context, random_target, -amount, allow_self=True)
            command_queue.append(("random", context, (random_target, -amount)))
        elif additional_targets:
            selected_members = list(additional_targets).copy()
            selected_members.append(target)
            if selected_members is None: return
            random_target = selected_members[random.randint(0, len(selected_members)-1)]
            command_queue.append(("", context, (random_target, -amount)))
        else:
            # await self.adjust_credit(context, target, -amount)
            command_queue.append(("", context, (target, -amount)))
        return

    @app_commands.command(
        name="toxicity",
        description="Report a toxic individual."
    )
    @app_commands.describe(
        target="The @ of the person you want to target. Leave empty to choose a random individual"
    )
    async def toxicity_slash(self, context: commands.Context, target: str = "random"):
        author_id = context.author.id

        current_time = time.time()
        if author_id not in config.user_toxicity_timer:
            config.user_toxicity_timer[author_id] = current_time
        elif current_time - config.user_toxicity_timer[author_id] < TOXICITY_COOLDOWN:
            time_difference = int(current_time - config.user_toxicity_timer[author_id])
            await utils.send_context_message(context, f"Can't use that command yet! Wait {TOXICITY_COOLDOWN - time_difference} seconds and try again.")
            return
        
        config.user_toxicity_timer[author_id] = current_time
        amount = random.randint(1, 100)
        
        if "rand" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            # await self.adjust_id_credit(context, random_target, -amount, allow_self=True)
            command_queue.append(("random", context, (random_target, -amount)))
        else:
            # await self.adjust_credit(context, target, -amount)
            command_queue.append(("", context, (target, -amount)))
        return


    @commands.command(
        name="generosity",
        description="Support a positive individual."
    )
    async def generosity(self, context: commands.Context, target: str = "random", *additional_targets):
        amount = random.randint(1, 100)

        if "rand" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            # await self.adjust_id_credit(context, random_target, amount, allow_self=True)
            command_queue.append(("random", context, (random_target, amount)))
        elif additional_targets:
            selected_members = list(additional_targets).copy()
            selected_members.append(target)
            if selected_members is None: return
            random_target = selected_members[random.randint(0, len(selected_members)-1)]
            command_queue.append(("", context, (random_target, amount)))
        else:
            # await self.adjust_credit(context, target, amount)
            command_queue.append(("", context, (target, amount)))
        return

    @app_commands.command(
        name="generosity",
        description="Support a positive individual."
    )
    @app_commands.describe(
        target="The @ of the person you want to target. Leave empty to choose a random individual"
    )
    async def generosity_slash(self, context: commands.Context, target: str = "random"):
        amount = random.randint(1, 100)

        if "rand" in target.lower():
            members = [member.id for member in context.guild.members]
            random_target = members[random.randint(0, len(members)-1)]
            # await self.adjust_id_credit(context, random_target, amount, allow_self=True)
            command_queue.append(("random", context, (random_target, amount)))
        else:
            # await self.adjust_credit(context, target, amount)
            command_queue.append(("", context, (target, amount)))
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
     
    @tasks.loop(seconds=1)
    async def handle_command_queue(self):
        if len(command_queue) == 0: return ""
        
        command_modifier, context, params = command_queue.pop(0)

        match command_modifier:
            case 'equality':
                toxicity_target, generosity_target, amount = params
                message = await self.adjust_id_credit(context, generosity_target, amount, allow_self=True, send_message=False) + "\n"
                message += await self.adjust_id_credit(context, toxicity_target, -amount, allow_self=True, send_message=False)
                await utils.send_context_message(context, message)
            case 'random':
                target, amount = params
                await self.adjust_id_credit(context, target, amount, allow_self=True)
            case 'random_id':
                target_id, amount = params
                await self.adjust_id_credit(context=context, target_id=target_id, amount=amount, allow_self=True)
            case 'id':
                target_id, amount = params
                await self.adjust_id_credit(context, target_id, amount)
            case _:
                target, amount = params
                await self.adjust_credit(context=context, target=target, amount=amount)

        return

async def setup(bot):
    await bot.add_cog(SocialCredit(bot))
    return

async def teardown(bot):
    await bot.remove_cog(SocialCredit(bot))
    return 
