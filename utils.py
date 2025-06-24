import re
import discord
from discord.ext import commands

def find_user_id(user: str) -> int:
    # Returns the User ID given the user mention.
    match_user: re.Match|None = re.match(r"<@!?(\d+)>", user)
    return -1 if match_user == None else int(match_user.group(1))

async def send_context_message(context: commands.Context, message: str):
    try:
        await context.send(message)
    except:
        await context.channel.send(message)
    return
