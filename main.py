import os
import sys

import discord
from discord.ext import commands

#LOCAL FILE IMPORTS
import config

sys.path.insert(0, 'cogs/')
from cogs import *

class SnekSupportBot(commands.Bot):
    def __init__(self, command_prefix): 
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents)
        pass

    async def setup_hook(self):
        errored_extensions = []
        for extension in config.extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded extensions \'{extension}\'")
            except Exception as exception:
                print(
                    f"Failed to load extensions \'{extension}\'\n" +
                    f"{type(exception).__name__}: {exception}"
                )
                errored_extensions.append(extension)
            
            print(f"Loaded extensions: {[x for x in self.cogs]}")
        
        for extension in errored_extensions: 
            config.extensions.remove(extension)

        return

bot = SnekSupportBot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name = "Captain Claw (1997)"))
    return

@bot.command()
async def load(context, extension):
    for config_extension in config.extensions:
        if config_extension == extension:
            print(f"Extension {config_extension} already exists!")
            return

    try:
        await bot.load_extension(extension)
        print(f"Loading extension {extension}")
        config.extensions.append(extension)
    except Exception as exception:
        print(f"Failed to load extension {extension}\n{type(exception).__name__}: {exception}")
    return

@bot.command()
async def unload(context, extension):
    if extension not in config.extensions:
        print(f"Extension {extension} either does not exist, or is not currently loaded")
        return

    try:
        await bot.unload_extension(extension)
        print(f"Unloading extension {extension}")
        config.extensions.remove(extension)
    except Exception as exception:
        print(f"Failed to unload extension {extension}\n{type(exception).__name__}: {exception}")
    return

@bot.command()
async def reload(context, extension):
    if extension not in config.extensions:
        print(f"Extension {extension} either does not exist, or is not currently loaded")
        return

    try:
        await bot.reload_extension(extension)
        print(f"Reloading extension {extension}")
    except Exception as exception:
        print(f"Failed to reload extension {extension}\n{type(exception).__name__}: {exception}")
    return

@bot.command()
async def update(context):
    try:
        os.system("git pull")
    except Exception as exception:
        print(f"{type(exception).__name__} : {exception}")

    for extension in config.extensions:
        try:
            await bot.reload_extension(extension)
            print(f"Reloading extension {extension}")
        except Exception as exception:
            print(f"Failed to reload extension {extension}\n{type(exception).__name__}: {exception}")
    return

@bot.command()
async def getloaded(context):
    message = "Currently Loaded extensions:\n"
    for i, extension in enumerate(config.extensions):
        message += f"{i+1}. {extension}\n"
    await context.channel.send(message)
    return

bot.run(config.token)
