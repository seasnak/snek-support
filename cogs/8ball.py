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

    @commands.command(
        help = "ask me a question (usage: ask a yes/no question no ! command necessary)"
    )
    async def eightBall(self, ctx):

        rand = random.randint(0, len(responses)-1)
        await ctx.channel.send(responses[rand])
        return

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user: return #don't reply to self
        question = ""
        try:
            question = ctx.content.lower().split()[0]
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
        if question in ['is', 'are', 'do', 'should', 'would', 'could', 'may', 'am', 'will', 'can', 'have', 'does', 'was', 'did']:
            rand = random.randint(0, len(responses)-1)
            await ctx.channel.send(responses[rand])
        return

    @commands.command(
        help = "list all responses"
    )
    async def responses(self, ctx, option = ""):
        # if options.startswith('a'): #add response
        message = ""
        for i in range(len(responses)):
            message += f"{i-1}. {responses[i]}\n"
        await ctx.channel.send(message)
        return

    @commands.command()
    async def response_add(self, ctx, response):
        responses.append(response)
        print(f"Added new response to 8ball: {response}")
        return

    @commands.command(alias = "response_remove")
    async def response_rm(self, ctx, num: int):
        print(f"Removed reponse: {responses.pop(num-1)}")
        return


def setup(bot):
    bot.add_cog(EightBall(bot))

def teardown(bot):
    bot.remove_cog(EightBall(bot))
