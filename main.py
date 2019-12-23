import discord
import random
from jikanpy import Jikan
import jikanpy
import time
from pprint import pprint
from urllib.request import Request
from urllib.request import urlopen

TOKEN  = open('secret.txt','r').read().split()[0].split('=')[1] #Change to JSON later

client = discord.Client()
jikan = Jikan()

eight_ball = ["That's not a question for a ~~bot~~ human ya know", "That's probably a no, but I ain't no question doctor", "Is Sekiro a hard game?", "Is Comm a useful major?",
            "There's literally one possible answer to that question, and it starts with a \'y\'", "That's a no from me", "Yes...?",
            "I was programmed to tell you just how stupid that question you just asked was, and to tell you the answer is a \'no\'.",
            "Yeah no.", "||Imagine clicking on a spoiler, just to have someone telling you that you are wrong||", "Ye"
            ] #contains all the eight ball responses

genre_ids = ['action', 'adventure', 'cars', 'comedy', 'dementia', 'demons', 'mystery', #split into rows of 7
            'drama', 'ecchi', 'fantasy', 'game', 'hentai', 'historical', 'horror',
            'kids','magic', 'martial arts', 'mecha', 'music', 'parody', 'samurai',
            'romance','school', 'sci-fi', 'shoujo', 'shoujo ai', 'shounen', 'shounen ai',
            'space','sports', 'super power', 'vampire', 'yaoi', 'yuri', 'harem',
            'slice of life', 'supernatural', 'military', 'police', 'psychological', 'thriller', 'seinen',
            'josei']

previous_questions = {}

class incorrectInfoError(Exception):
    pass

@client.event
async def on_message(message):
    message_string = message.content.lower()
    command_list = message_string.split()
    command = message_string[0]
    #print(message_string)

    if message.author == client.user:   #do not reply to yourself/another bot
        #print(f"message \"{message}\" is from a bot")
        return

    if message.content.startswith('!hello'):    #test command, !hello
        await message.channel.send(f"Hello {message.author.mention}")
        return

    if message_string.startswith(('is', 'are', 'do', 'should', 'would', 'could', 'may', 'am', 'will', 'can')):
        print(previous_questions)
        if f'{message.author}?{message_string}' in previous_questions:
            #print("key is in dictionary")
            await message.channel.send(f"Nice try, I'm not answering that again {message.author.mention}")
            return
        rand_number = random.randint(0, len(eight_ball))
        eight_ball_msg = eight_ball[rand_number]
        if eight_ball[rand_number] is "What do you think?":
            await messsage.add_reaction('👍')
            await message.add_reaction('👎')
        eight_ball_msg = f"{message.author.mention} {eight_ball_msg}"
        previous_questions[f"{message.author}?{message_string}"]=eight_ball_msg
        await message.channel.send(eight_ball_msg)
        return

    if message_string.startswith('!anime_test'):
        print("testing stuff :3")
        num_results = 0
        request = Request('https://api.jikan.moe/v3/genre/anime/1/1')
        anime_info = urlopen(request).read().decode("ascii").split(',')
        for info in anime_info:
            if info.startswith('\"item_count\"'):
                num_results = info.split(':')[1]
                print(num_results)
                return
        return

    if message_string.startswith('!anime'):
        #print(jikan.anime(1).get('genres'))
        #genre = "default" #did the user specify a genre
        genres = []
        genres_strings = []
        genres_list = [] #list of genres that anime contains
        season = [] #desired season
        name = ""
        score = 10
        num = 1

        if "-help" in command_list:
            await message.channel.send(f"-genre <genre 1> <genre 2> ...: search by genre \n-genre_list: list all genres \n-season <season> <year>: list anime in a specific genre \n-random: return a random anime (can be paired with genre) \n-name <name>: returns the specified anime \n-score <value>: only returns anime with a score >= passed score")
            return

        if "-genre_list" in command_list:
            await message.channel.send(f"{genre_ids}")
            return

        if "-genre" in command_list: #did the user specify genres?
            genre_finder = message_string.split('-')
            for i in genre_finder:
                if i.split()[0].startswith('genre'):
                    for j in i.split():
                        if j != "genre": #don't want to add genre to the list
                            if ".." in j: #for genres that are 2+ words, use .. instead of a space
                                k = ""
                                for word in j.split('..'):
                                    k+=word + " "
                                j = k
                            if j not in genre_ids:
                                await message.channel.send(f"genre {j} doesn't exist. Type \'!anime -list_genres\' to see all genres")
                                return
                            if "-random" in command_list:
                                genres_strings.append(j)
                            else:
                                genres.append(genre_ids.index(j)+1)


        if "-score" in command_list:
            score_finder = message_string.split('-')
            for i in score_finder:
                if i.split()[0].startswith('score'):
                    score = int(i.split()[1])

        elif "-season" in command_list:
            season_finder = message_string.split('-')
            for i in season_finder:
                if i.split()[0].startswith('season'):
                    for j in i.split():
                        if j!= 'season':
                            season.append(j)

        elif "-name" in command_list:
            genre_finder = message_string.split('-')
            for i in genre_finder:
                if i.split()[0].startswith('name'):
                    name = i.split()[0].split()[1] #getting the anime name

        if "-random" in command_list:
            rand_number = random.randint(1, 35000)
            is_anime = False
            #print(jikan.anime(1)) #test anime to see parameters
            while not is_anime:
                try:
                    for g in jikan.anime(rand_number).get('genres'):
                        genres_list.append(g.get('name').lower())
                    if len(genres_strings) is 0 or set(genres_strings).issubset(set(genres_list)):
                        print(f"Found anime with genres {genres_list}")
                        await message.channel.send(jikan.anime(rand_number).get('title') + ": " + jikan.anime(rand_number).get('url'))
                        is_anime = True
                    else:
                        raise incorrectInfoError
                except jikanpy.exceptions.APIException:
                    print("404 Error, trying again")
                    genres_list.clear()
                    rand_number = random.randint(1, 35000)
                except incorrectInfoError:
                    print(genres_list)
                    print("Incorrect Genre, Searching Again")
                    genres_list.clear()
                    rand_number = random.randint(1, 35000)
        else: #search
            num_results = 0
            request = Request(f'https://api.jikan.moe/v3/genre/anime/{genres[0]}/1')
            anime_info = urlopen(request).read().decode("ascii").split(',')
            for info in anime_info:
                if info.startswith('\"item_count\"'):
                    num_results = int(info.split(':')[1])
            page_number = random.randint(1, int(num_results/50))
            print(num_results)

            if len(genres) > 0:
                search_result = jikan.search('anime', page=page_number, query="", parameters={'genre':genres[0]})
            elif name != "":
                search_result = jikan.search('anime', name)
            elif len(season) > 0:
                search_result = jikan.season(year=int(season[1]), season=season[0])
            else:
                await message.channel.send('What do you want to search? Type \'!anime -help\' for all options')

            for i in range(num):
                num_results = len(search_result['results'])
                #print(search_result['results'])
                try:
                    result = search_result['results'][random.randint(0, num_results-1)]
                except ValueError:
                    print("No anime found on that page")
                await message.channel.send(result.get('title') + ': ' + result.get('url'))

            return

    if message_string.startswith('!poll'): #geneartes a poll
        #format is !poll <question> | <option a> | <option b> | <option c> | ... | <option z>
        # print(f"poll is for: {message_string}")
        poll_option = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:", ":regional_indicator_e:",
            ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:", ":regional_indicator_i:"]
        count = 0
        poll_string = message.content.split('|')
        if len(poll_string) < 3:
            print("Insufficient arguments")
            return
        question = poll_string[0][6:] #question without !poll
        options = poll_string[1:]
        print(f"Creating Poll: {question}: {options}")
        poll = discord.Embed(title = question, color=message.author.color)
        poll.set_author(name=message.author)
        for option in options:
            poll.add_field(name=f"option {poll_option[count]}:", value=f"{option}", inline=False)
            count+=1
        poll_message = await message.channel.send(embed=poll)
        for i in range(count):
            await poll_message.add_reaction(poll_option[i].replace(":", ""))
        return

    if message_string.startswith(f'who are you {client.user.mention}'):
        await message.channel.send(f"Hello, {message.author.mention} I am a nice human who gives sometimes good info, and helps around with stuff in this peaceful bunghole")
        return

    if "owo" in message_string:
        message_string = message.content.replace("r", "w")
        message_string = message_string.replace("ll", "w")
        message_string = message_string.replace("l", "v")
        message_string = message_string.replace("ie", 'e')
        await message.channel.send(message_string)

    if message.content.lower().startswith('define')
        msg_split = message.content.lower().split('define ')
        embed = discord.Embed(title = msg_split[1], color=message.author.color)
        embed.set_author(name=message.author)
        try:
            print('getting defintion from: https://www.merriam-webster.com/dictionary/' + msg_split[1].replace(' ', '%20'))
            with urllib.request.urlopen('https://www.merriam-webster.com/dictionary/' + msg_split[1].replace(' ','%20')) as response:
                tmp_definition = ""
                definition = ""
                count = 1
                for line in response:
                    line = line.decode('utf-8')
                    if 'definition is -' in line:
                        tmp_definition = line.split('definition is - ')[1]
                        tmp_definition = tmp_definition[:tmp_definition.find('How to use')].replace('">','')
                        tmp_definition = tmp_definition.split("<")[0]
                        definition += f"{count}. " + tmp_definition + "\n"
            embed.add_field(name="Merriam-Webster:", value=definition, inline=False)
            print(definition)
            definition = ""

        except urllib.error.HTTPError:
            print("Could not find a defintion from Merriam Webster")

        try:
            print('getting definition from: https://www.urbandictionary.com/define.php?term=' + msg_split[1].replace(' ','+'))
            with urllib.request.urlopen('https://www.urbandictionary.com/define.php?term=' + msg_split[1].replace(' ','+')) as response:
                count = 1
                tmp_definition = ""
                definition = ""
                has_multiple = False #used to keep track of multiple definitions within 1 definition
                for line in response:
                    line = line.decode('utf-8')
                    if '<div class="meaning">' in line:
                        result = re.search('<div class="meaning">(.*)<div class="example">', line)
                        tmp_definition = re.sub(r'<[^>]+>', '', result.group(1)).replace('&apos;',"'").replace('&quot;','"')
                        if "1." in tmp_definition:
                            has_multiple = True
                        tmp_definition = tmp_definition.replace("1.", " a.")
                        if has_multiple:
                            tmp_definition = tmp_definition.replace("2.", "\n  b.")
                            tmp_definition = tmp_definition.replace("3.", "\n  c.")
                            tmp_definition = tmp_definition.replace("4.", "\n  d.")
                            tmp_definition = tmp_definition.replace("5.", "\n  e.")
                            has_multiple = False
                        tmp_definition = f"{count}. " + tmp_definition + "\n"
                        if len(definition + tmp_definition) <= 1024:
                            definition += tmp_definition
                            count += 1

                    if count > 5:
                        embed.add_field(name="Urban Dictionary:", value=definition, inline=False)
                        print(definition)
                        await message.channel.send(embed=embed)
                        break
            embed.add_field(name="Urban Dictionary:", value=definition, inline=False)
        except urllib.error.HTTPError:
            print("Could not find a definition from Urban Dictionary")
        await message.channel.send(embed=embed)
        break

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}@{client.user.id}')
    print('--------------------------------------------------')

client.run(TOKEN)
