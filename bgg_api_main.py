import bgg_api_func as bgg
from termcolor import colored
# Text colors:
    # grey, red, green, yellow, blue, magenta, cyan, white
# Text highlights:
    # on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white
# Attributes:
    # bold, dark, underline, blink, reverse, concealed

# cprint('Hello, World!', 'green', 'on_red')
# text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])

#? Test with: Railways of the World (name is different on output)
#? Test with: Clash of Decks / Clash of DEKS


bgg.set_download_folder()


while True:
    game_selected = ""
    game_id = ""
    is_game_found = False
    love_exact_src = True

    user_game = input("What's the game you are looking for? ")

    try:
        game_selected = bgg.exact_src(user_game)
        is_game_found = bgg.game_selection(game_selected)
        if not is_game_found:
            raise AttributeError
    except AttributeError:
        print(colored("Name doesn't match", "magenta"))
        
        while not is_game_found:
            user_inp = input("Do you want to see similar games? (y/n) \n")
            if user_inp == 'n':
                break
            elif user_inp == "y" or user_inp == '':
                bg_list = bgg.broad_src(user_game)

                while not is_game_found: #! if no matches.. say it!
                    user_num = input("\nChoose a number from the list or quit (q) ")  #TODO: Sort: default by name, choose year (or back to name if year)
                    if user_num == "q":
                        is_game_found = True
                    else:
                        try:
                            game_selected = bg_list[int(user_num) - 1]
                            is_game_found = bgg.game_selection(game_selected)
                        except ValueError:
                            print(colored("I need a number.. THANK YOU!", "red"))
                            continue

            else:
                print('Sorry? ')
                continue

    user_inp = input("New search? y/n ") #! Don't ask, just "New search or quit (q)"
    if user_inp == "n":
        print("Bye!")
        quit()
    elif user_inp == "y" or user_inp == '':
        continue
    else:
        print("I'll ask you again:", end='   ') #! broken, goes to top (which is good if ww ask for less stuff)

