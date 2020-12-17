
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
