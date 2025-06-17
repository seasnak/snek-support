import discord
from discord.ext import commands
import os
import subprocess
import random
import sys

#LOCAL FILE IMPORTS
import config

sys.path.insert(0, 'cogs/')
from cogs import *

bot = commands.Bot(command_prefix='!')

class SnekSupportBot:
    def __init__(self, command_prefix, intents): 
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        return

    async def setup_hook(self):
        # load extensions 
        errored_extensions = []
        for extension in config.extensions:
            try:
                await bot.load_extension(extension)
                print(f"Loaded extensions \'{extension}\'")
            except Exception as e:
                print(f"Failed to load extensions \'{extension}\' \n{type(e).__name__}: {e}")
                errored_extensions.append(extension)
            
            print(f"Loaded extensions: {[x for x in bot.cogs]}")
        
        for extension in errored_extensions: 
            config.extensions.remove(extension)
            
        return

        return

# @bot.event
# async def on_message(message):
#     if message.author == bot.user: return #message was sent by self
#     return

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name = "Light Mode"))
    return

@bot.command()
async def load(ctx, ext):
    for extension in config.extensions:
        if extension == ext:
            print(f"Extension {ext} already exists!")
            return

    try:
        bot.load_extension(ext)
        print(f"Loading extension {ext}")
        config.extensions.append(ext)
    except Exception as e:
        print(f"Failed to load extension {ext}\n{type(e).__name__}: {e}")
    return

@bot.command()
async def unload(ctx, ext):
    if ext not in config.extensions:
        print(f"Extension {ext} either does not exist, or is not currently loaded")
        return

    try:
        bot.unload_extension(ext)
        print(f"Unloading extension {ext}")
        config.extensions.remove(ext)
    except Exception as e:
        print(f"Failed to unload extension {ext}\n{type(e).__name__}: {e}")
    return

@bot.command()
async def reload(ctx, ext):
    if ext not in config.extensions:
        print(f"Extension {ext} either does not exist, or is not currently loaded")
        return

    try:
        bot.reload_extension(ext)
        print(f"Reloading extension {ext}")
    except Exception as e:
        print(f"Failed to reload extension {ext}\n{type(e).__name__}: {e}")
    return

@bot.command()
async def update(ctx):
    try:
        os.system("git pull")
    except Exception as e:
        print(f"{type(e).__name__} : {e}")

    for extension in config.extensions:
        try:
            bot.reload_extension(extension)
            print(f"Reloading extension {extension}")
        except Exception as e:
            print(f"Failed to reload extension {extension}\n{type(e).__name__}: {e}")
    return

# @bot.command()
# async def sys(ctx, *, message):
#     print(f"bash: {message}")
#     if f"{ctx.author.id}" not in config.admins: return
#     try:
#         output = subprocess.check_output(message)
#         await ctx.channel.send(output.decode("utf-8"))
#     except Exception as e:
#         print(f"{type(e).__name__} : {e}")
#     return

@bot.command()
async def getloaded(ctx):
    message = "Currently Loaded Extensions:\n"
    i = 1
    for extension in config.extensions:
        message += f"{i}. {extension}\n"
        i += 1
    await ctx.channel.send(message)
    return

bot.run(config.token) #run bot

# if __name__ == "__main__":
#     # print(config.extensions)
#     for ext in config.extensions:
#         try:
#             bot.load_extension(ext)
#             print(f"Loading extension {ext}")
#         except Exception as e:
#             print(f"Failed to load extension {ext}\n{type(e).__name__}: {e}")
#
