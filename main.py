import discord
import random
import base64

secret_dict = {}

client = discord.Client()


def populate_dict(dict, text):
    elements = open(text, 'r').read().split() # getting SECRETs
    for value in elements:
        value = value.split(":")
        dict.update({value[0]: value[1]})
    return dict

@client.event
async def on_message(message):
    message_string = message.content.lower()
    command_list = message_string.split()
    command = message_string[0]
    print(message_string) #DEBUG

    if message.author == client.user: return
    
    return

@client.event
async def on_ready():
    print(f"Logged in as {client.user}".format(client))
    return

if __name__ == "__main__":
    populate_dict(secret_dict, "secret.txt")

    client.run(secret_dict['token']) #run bot
