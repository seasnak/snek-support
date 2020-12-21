from discord.ext import commands
import discord
import random

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @commands.command()
    async def anime(self, ctx):
        """Anime Search Command"""
        rand = random.randint(0, 99)
        if rand == 1:
            embed = discord.Embed(
                title = "Cory in the House",
                url = "https://www.youtube.com/watch?app=desktop&v=KumtJtNqiT0",
                color = ctx.author.color
            )
            embed.set_thumbnail(url="https://m.media-amazon.com/images/M/MV5BMTUzOTU1MjY3M15BMl5BanBnXkFtZTcwMTUyMTk0MQ@@._V1_UY268_CR4,0,182,268_AL_.jpg")
            embed.add_field(name="Genre", value="Comedy, Family", inline=True)
            embed.add_field(name="Year", value="2007-2008", inline=True)
            embed.set_footer(text="anime search result")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("weeb.")
        return

    async def cory(self, ctx):
        """Cory in the House Roulette"""
        rand = random.randint(0, 99)
        if rand == 1:
            embed = discord.Embed(
                title = "Cory in the House",
                url = "https://www.youtube.com/watch?app=desktop&v=KumtJtNqiT0",
                color = ctx.author.color
            )
            embed.set_thumbnail(url="https://m.media-amazon.com/images/M/MV5BMTUzOTU1MjY3M15BMl5BanBnXkFtZTcwMTUyMTk0MQ@@._V1_UY268_CR4,0,182,268_AL_.jpg")
            embed.add_field(name="Genre", value="Comedy, Family", inline=True)
            embed.add_field(name="Year", value="2007-2008", inline=True)
            embed.set_footer(text="anime search result")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("weeb.")
        return

def setup(bot):
    bot.add_cog(Anime(bot))
