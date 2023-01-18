from bs4 import BeautifulSoup
from termcolor import colored
import urllib.request
import requests
import os

download_dir = ""
folder_name = "Images_BGG"
# is_exact_src = True
is_found_by_id = False


def set_download_folder():
    global download_dir
    while True:
        user_folder = input("Hello mate! I'll put the images in the Download folder, is that ok? (y/n) ")
        if user_folder == "y" or user_folder == '':
            download_dir = "/Users/Ale/Downloads"
            break
        elif user_folder == "n":
            download_dir = input("Ok, tell me the path to the folder (ex: /Users/Ale/Downloads): ")
            break
        else:
            print("What did you say? \n")
            continue


def find_game_data(game_to_find, is_exact_src=True):
    """Returns the html for the page of the game_to_find
       game_to_find = The title of the game
       is_exact_src = True if you want to search the exact title """
    exact = 1 if is_exact_src else 0
    game_name_f = '%20'.join(game_to_find.split(' '))
    response_game = requests.get(
        f'https://www.boardgamegeek.com/xmlapi/search?search={game_name_f}&exact={exact}&type=boardgame').text
    soup = BeautifulSoup(response_game, 'lxml')
    return soup


def exact_src(game):
    soup = find_game_data(game, True)
    games_list = soup.find_all("boardgame")

    chosen_game = soup.find("boardgame")

    for g in games_list: #Check if it's the primary name for the game, if not remove
        if not is_primary_name(g):
            games_list.remove(g)

    prev_game_year = 0

    same_year_games = []
    
    for game in games_list:
        if game_year(game) == "----":
            continue

        current_game_year = int(game_year(game))

        if current_game_year > prev_game_year:
            prev_game_year = current_game_year
            chosen_game = game
            same_year_games.clear() # FROM HERE A: Not tested yed
            same_year_games.append(game)
        elif current_game_year == prev_game_year:
            same_year_games.append(g) # TO HERE A: Not tested yet    


    if len(same_year_games) > 1:
        for count, g in enumerate(same_year_games, 1):
            print(f'{count} - {game_name(g)} ({game_year(g)} - id:{game_id(g)})')

        while True: # FROM HERE B: Not tested yed
            user_num = input(f'There are {len(same_year_games)} games with this name, published the same year, which one do you need?')
            try:
                chosen_game = same_year_games[int(user_num)]
                break
            except ValueError:
                print(colored("I need a number.. THANK YOU!", "red"))
                continue # TO HERE B: Not tested yet

    return chosen_game


def broad_src(game):
    soup = find_game_data(game, False)
    bg = soup.find_all("boardgame")

    game_list = []
    i = 1

    for g in bg:
        if is_primary_name(g): # Exclude translations
            game_list.append(g)

    game_list_sorted_name = sorted(game_list, key=game_name)
    game_list_sorted_year = sorted(game_list, key=game_year) ## TODO: Let user choose
            
    for g in game_list_sorted_name:
        print(f"{i} - ({game_year(g)}) {game_name(g)} => id: {game_id(g)}")
        i += 1

    return game_list_sorted_name


def id_src(g_id):
    response_stats = requests.get(f'https://www.boardgamegeek.com/xmlapi/boardgame/{g_id}?stats=1').text
    soup = BeautifulSoup(response_stats, 'lxml')
    return soup


def game_name(g):
    return g.find("name").text


def is_primary_name(game):
    if game.find(attrs={"primary" : "true"}) == None:
        return False
    else:
        return True


def game_id(g):
    g_id = (str(g)).split('"')[1]
    return g_id


def game_year(g):
    try:
        g_year = g.find("yearpublished").text
        return g_year
    except AttributeError:
        return "0000"
        # return "----"


def game_selection(game_selected):
    name = game_name(game_selected)
    year = game_year(game_selected)
    g_id = game_id(game_selected)
    while True:
        user_inp2 = input(f"Is '{name} ({year})' the game you are looking for? (y/n) ")
        print("- - - - - - - -")
        if user_inp2 == "y" or user_inp2 == '':
            get_game_stats(id_src(g_id), g_id)
            return True
        elif user_inp2 == "n":
            return False


def get_game_stats(soup, g_id):
    title = soup.find("name").text
    year = soup.find("yearpublished").text
    min_pl = soup.find("minplayers").text
    max_pl = soup.find("maxplayers").text
    min_t = soup.find("minplaytime").text
    max_t = soup.find("maxplaytime").text
    rating = round(float(soup.find("average").text), 1)
    age = soup.find("age").text

    pl = f"{min_pl} Player" if min_pl == max_pl else f"{min_pl}-{max_pl} Players"
    t = min_t if min_t == max_t else f"{min_t}-{max_t}"

    g_info = colored(f"{title} ({year}): {pl}, {t} Min, {age}+, <{rating}>", "cyan")
    print(g_info)
    print(f"Link: https://boardgamegeek.com/boardgame/{g_id}\n")

    img_download(soup, g_info)


def img_download(soup, g_info):
    while True:
        user_download = input("Do you want to download the image? (y/n) ")
        if user_download == "n":
            break
        elif user_download == "y" or user_download == '':
            final_dir = os.path.join(download_dir, folder_name)
            if not os.path.exists(final_dir):
                os.mkdir(final_dir)
            os.chdir(final_dir)
            for e in os.listdir():
                if e[:-4] == g_info:
                    print(colored("Already there buddy! \n", "green"))
                    break
            img_url = soup.find("image").text
            urllib.request.urlretrieve(img_url, f"{g_info}.jpg")
            break
        else:
            print("Missclicked? \n")
            continue

