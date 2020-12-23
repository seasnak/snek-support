from discord.ext import commands
import discord
import random
import config

boomers = []

non_boomers = []

class Boomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        for person in config.boomers:
            boomers.append(person)
            print(f"Added {person} to boomers list")
        for person in config.admins:
            boomers.append(person)
            print(f"Added {person} to boomers list")
        return

    @commands.command()
    async def boomer(self, ctx, person):
        person_id = person[3:-1]
        if person_id in boomers:
            await ctx.channel.send(f"{person}\'s fate has already been decided. They are a boomer.")
            return
        elif person_id in non_boomers:
            await ctx.channel.send(f"{person}\'s fate has already been decided. They are a non-boomer.")
            return
        elif f"{ctx.author.id}" in non_boomers:
            await ctx.channel.send(f"Begone non-boomer!")
            return
        elif f"{ctx.author.id}" not in boomers:
            await ctx.channel.send(f"Only boomers can use this command")
            return

        rand = random.randint(0, 99)
        if rand > 50:
            boomers.append(person_id)
            await ctx.channel.send(f"{person} is definitely a boomer. Welcome to the Boomer Brotherhood!")
        else:
            non_boomers.append(person_id)
            await ctx.channel.send(f"{person} is not a boomer. Too Bad!")
        return

def setup(bot):
    bot.add_cog(Boomer(bot))

def teardown(bot):
    bot.remove_cog(Boomer(bot))
