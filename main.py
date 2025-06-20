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
                await self.load_extension(f"cogs.{extension}")
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
    await bot.change_presence(activity=discord.Game(name = "Snake Bird", type=discord.ActivityType.playing))

    SNEKGUILD_ID = 1361576958923767899
    snek_guild = discord.Object(id=SNEKGUILD_ID)
    bot.tree.copy_global_to(guild=snek_guild)
    await bot.tree.sync(guild=snek_guild)
    print("Commands synced")
    return

@bot.hybrid_command(
    name="load",
    description="Load an extension. See !extensions for a list of available extensions.",
)
@commands.is_owner()
async def load(context: commands.Context, extension: str):
    extension = extension.strip()
    try:
        await bot.load_extension(f"cogs.{extension}")
        print(f"Loaded extension \'{extension}\'.")
        await context.send(f"Loaded extension \'{extension}\'.")
        config.extensions.append(f"{extension}")
    except commands.ExtensionNotFound:
        await context.send(f"Error: Extension \'{extension}\' not found.")
    except commands.ExtensionAlreadyLoaded:
        await context.send(f"Error: Extension \'{extension}\' already loaded.")
    except Exception as exception:
        print(f"Failed to load extension {extension}\n{type(exception).__name__}: {exception}")
        await context.send(f"Failed to load extension \'{extension}\'.")
    return

@bot.hybrid_command(
    name="unload",
    description="Unload an extension. See !loaded for a list of currently loaded extensions."
)
@commands.is_owner()
async def unload(context: commands.Context, extension: str):
    extension = extension.strip()
    try:
        await bot.unload_extension(f"cogs.{extension}")
        await context.send(f"Unloaded extension \'{extension}\'.")
        config.extensions.remove(f"{extension}")
    except commands.ExtensionNotFound:
        await context.send(f"Error: Extension \'{extension}\' not found.")
    except commands.ExtensionAlreadyLoaded:
        await context.send(f"Error: Extension \'{extension}\' already loaded.")
    except Exception as exception:
        print(f"Failed to unload extension \'{extension}\'. \n{type(exception).__name__}: {exception}")
        await context.send(f"Failed to unload extension \'{extension}\'.")
    return

@bot.hybrid_command(
    name="reload",
    description="Reload an extension. See !loaded for a list of currently loaded extensions."
)
@commands.is_owner()
async def reload(context: commands.Context, extension: str):
    extension = extension.strip()
    print(f"Reloading extension \'{extension}\'")
    try:
        await bot.reload_extension(f"cogs.{extension}")
        await context.send(f"Reloaded extension \'{extension}\'")
    except commands.ExtensionNotFound:
        await context.send(f"Error: Extension \'{extension}\' not found.")
        print(f"ExtensionNotFound Error: Extension \'{extension}\' not found.")
    except commands.ExtensionAlreadyLoaded:
        await context.send(f"Error: Extension \'{extension}\' already loaded.")
        print(f"Error: Extension \'{extension}\' already loaded.")
    except Exception as exception:
        await context.send(f"Failed to reload extension \'{extension}\'.")
        print(f"Error reloading extensions \'{extension}\'. \n{type(exception).__name__}: {exception}")
    return

@bot.hybrid_command(
    name="update",
    description="Downloads any updates and reloads all extensions.",
)
@commands.is_owner()
async def update(context: commands.Context):
    try:
        os.system("git pull")
    except Exception as exception:
        print(f"{type(exception).__name__} : {exception}")
        await context.send("Error: Failed to pull update from git.")

    for extension in config.extensions:
        try:
            await bot.reload_extension(extension)
            print(f"Reloading extension {extension}")
        except Exception as exception:
            print(f"Failed to reload extension {extension}\n{type(exception).__name__}: {exception}")
    await context.send("Successfully updated.")
    return

@bot.hybrid_command(
    name="loaded",
    description="Lists all currently loaded extensions",
)
async def loaded(context: commands.Context):
    message = "Currently Loaded extensions:\n"
    for i, extension in enumerate(config.extensions):
        message += f"{i+1}. {extension}\n"
    await context.send(message)
    return

@bot.hybrid_command(
    name="extensions",
    description="Lists all available extensions."
)
async def extensions(context: commands.Context):
    await context.send("Not implemented (yet).")
    return

@bot.hybrid_command(
    name="ping",
    description="pong!"
)
async def ping(context: commands.Context):
    await context.send("pong!")
    return

bot.run(config.token)
