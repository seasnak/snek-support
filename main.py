import discord
from discord.ext import commands
import os
import random

#LOCAL FILE IMPORTS
from cogs import *
import config
import hello
import anime

secret_dict = {}

bot = commands.Bot(command_prefix='!')

def populate_dict(dict, text):
    elements = open(text, 'r').read().split() # getting SECRETs
    for value in elements:
        value = value.split(":")
        dict.update({value[0]: value[1]})
    return dict

# @bot.event
# async def on_message(message):
#     if message.author == bot.user: return #message was sent by self
#     return

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
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
        config.extension.append(ext)
    except Exception as e:
        print(f"Failed to load extension {ext}\nError: {type(e).__name__}: {e}")
    return

@bot.command()
async def unload(ctx, ext):
    if ext in config.extensions:
        print(f"Extension {ext} either does not exist, or is not currently loaded")
        return

    try:
        bot.unload_extension(ext)
        print(f"Unloading extension {ext}")
        config.extensions.remove(ext)
    except Exception as e:
        print(f"Failed to unload extension {ext}\nError: {type(e).__name__}: {e}")
    return

@bot.command()
async def reload(ctx, ext):
    if ext in config.extensions:
        print(f"Extension {ext} either does not exist, or is not currently loaded")
        return

    try:
        bot.reload_extension(ext)
        print(f"Reloading extension {ext}")
    except Exception as e:
        print(f"Failed to reload extension {ext}\nError: {type(e).__name__}: {e}")
    return

if __name__ == "__main__":
    populate_dict(secret_dict, "secret.txt")

    # print(config.extensions)
    for ext in config.extensions:
        try:
            bot.load_extension(ext)
            print(f"Loading extension {ext}")
        except Exception as e:
            print(f"Failed to laod extension {ext}\nError: {type(e).__name__}: {e}")

    bot.run(secret_dict['token']) #run bot
