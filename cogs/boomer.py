from discord.ext import commands
import discord
import random
import config

class Boomer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # for person in config.boomers:
        #     boomers.append(person)
        #     print(f"Added {person} to boomers list")
        # for person in config.admins:
        #     boomers.append(person)
        #     print(f"Added {person} to boomers list")
        return

    @commands.is_owner()
    @commands.command(hidden = True)
    async def list_users(self, ctx):
        print(f"boomers: {boomers}\nnon-boomers: {non_boomers}")
        await ctx.channel.send(f"boomers: {boomers}\nnon-boomers: {non_boomers}")
        return

    @commands.command(
        help = "determines if another user is a boomer",
        usage = "@<user>",
    )
    async def boomer(self, ctx, person):
        person_id = person[3:-1]
        if person_id in config.boomers:
            await ctx.channel.send(f"{person} are and will always be a boomer.")
            return
        elif person_id in config.non_boomers:
            await ctx.channel.send(f"{person} are and will always be a non-boomer.")
            return

        if f"{ctx.author.id}" in config.non_boomers:
            await ctx.channel.send(f"Begone non-boomer!")
            return
        elif f"{ctx.author.id}" not in config.boomers:
            await ctx.channel.send(f"Only boomers can use this command")
            return

        rand = random.randint(0, 1)
        if rand == 0:
            config.boomers.append(person_id)
            await ctx.channel.send(f"{person} is definitely a boomer. Welcome to the Boomer Brotherhood!")
        else:
            config.non_boomers.append(person_id)
            await ctx.channel.send(f"{person} is not a boomer. Too Bad!")
        return

def setup(bot):
    bot.add_cog(Boomer(bot))

def teardown(bot):
    bot.remove_cog(Boomer(bot))
