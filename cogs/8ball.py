from discord.ext import commands
import random

responses = [
            "That's not a question for a ~~bot~~ human ya know", "That's probably a no, but I ain't no question doctor", "Is Sekiro a hard game?", "Is Comm a useful major?",
            "There's literally one possible answer to that question, and it starts with a \'y\'", "That's a no from me", "Yes...?",
            "I was programmed to tell you just how stupid that question you just asked was, and to tell you the answer is a \'no\'.",
            "Yeah no.", "||Imagine clicking on a spoiler, just to have someone telling you that you are wrong||", "Ye"
            ] #contains all the eight ball responses

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eightBall(self, ctx):
        rand = random.randint(0, len(responses)-1)
        await ctx.channel.send(responses[rand])
        return

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user: return #don't reply to self
        question = ctx.content.lower()
        if question.startswith(('is', 'are', 'do', 'should', 'would', 'could', 'may', 'am', 'will', 'can')):
            rand = random.randint(0, len(responses)-1)
            await ctx.channel.send(responses[rand])
        return

    @commands.command()
    async def responses(self, ctx):
        message = ""
        for i in range(len(responses)):
            message += f"{i}. {responses[i]}\n"
        await ctx.channel.send(message)
        return

    @commands.command()
    async def response_add(self, ctx, response):
        responses.append(response)
        print(f"Added new response to 8ball: {response}")
        return

    @commands.command(alias = "response_remove")
    async def response_rm(self, ctx, num: int):
        print(f"Removed reponse: {responses.pop(num)}")
        return


def setup(bot):
    bot.add_cog(EightBall(bot))

def teardown(bot):
    bot.remove_cog(EightBall(bot))
