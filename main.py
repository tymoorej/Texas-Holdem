"""
This is the main file in our project. Every function from evrey other file
can be traced back to being called from here. It is also the file that contains
all the functions needed for visualization. Also contains a profiler to determine
the run time of all the functions we have implimented.
"""

from card import *
from winning_hand import winner
from bot import *
import cProfile
import argparse
import pygame
from visual_setup import *

# Setting up the parser
parser = argparse.ArgumentParser(
    description='Winning hand anaylsis.',
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '-p',
    '--profile',
    help="If on turns on profiler else runs regularly",
    action="store_true",
    dest='profiler')

args = parser.parse_args()

r = 0  # the round number, only used for testing


def start_screen():
    """
    This function initializes the start screen that the user will see when they
    first run the code, all it has on it is a background and a button advancing
    to the next screen.

    Inputs: None

    Outputs: None.

    Runtime: N/A since it runs until the user clicks "Start game"
    """
    global game_over

    Window.blit(Title_image, (0, 0))
    pygame.display.update()
    x = width / 2
    y = height / 2 - 200
    dx = 170
    dy = 35
    end = False
    over_top = False
    while end is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if over_top is True:
                    end = True
        Window.blit(Title_image, (0, 0))
        position = pygame.mouse.get_pos()
        if position[0] >= x and position[0] <= x + dx and position[1] >= y and position[1] <= y + dy:
            pygame.draw.rect(Window, grey, (x, y, dx, dy))
            over_top = True
        else:
            pygame.draw.rect(Window, white, (x, y, dx, dy))
            over_top = False
        myfont = pygame.font.SysFont("monospace", 25)
        start_label = myfont.render("Start Game", 1, black)
        Window.blit(start_label, (x, y))
        pygame.display.update()
        clock.tick(60)  # fps


def player_bet(current_call, player, bot, table, can_raise=True, done=False):
    """
    This function handels both the player's decision(whether to bet, fold, etc...)
    also while handelling all printing to the screen, it will run until the user
    makes a decision.

    Input:
    current call - the minimum amount of chips the bot must put in.
    bot - an object of the bot class, essentially our bot we will be playing against
    table - an object of the Table class
    can_raise=True - whether or not the bot is allowed to raise, default is True
    done=False - if done is enabled then we will display the bots cards and the
    winner if there is a winner

    Output: None.

    Runtime: N/A since it runs until the user makes a selection
    """
    global game_over
    Window.blit(empty_table, (0, 0))
    pygame.display.update()
    end = False

    card1 = player.get_cards()[0]
    card2 = player.get_cards()[1]

    name1 = get_file_name(card1)
    name2 = get_file_name(card2)

    first_card = pygame.image.load("PNG-cards-1.3/" + name1)
    first_card = pygame.transform.scale(first_card, (100, 145))

    second_card = pygame.image.load("PNG-cards-1.3/" + name2)
    second_card = pygame.transform.scale(second_card, (100, 145))

    if not done:
        facedown = pygame.image.load("PNG-cards-1.3/" + "facedown.jpg")
        facedown = pygame.transform.scale(facedown, (100, 145))
    if done:
        card1 = bot.get_cards()[0]
        card2 = bot.get_cards()[1]
        name1 = get_file_name(card1)
        name2 = get_file_name(card2)
        bot_first_card = pygame.image.load("PNG-cards-1.3/" + name1)
        bot_first_card = pygame.transform.scale(bot_first_card, (100, 145))

        bot_second_card = pygame.image.load("PNG-cards-1.3/" + name2)
        bot_second_card = pygame.transform.scale(bot_second_card, (100, 145))

    table_disp = []

    for c in table.get_cards():
        current_name = get_file_name(c)
        temp = pygame.image.load("PNG-cards-1.3/" + current_name)
        temp = pygame.transform.scale(temp, (100, 145))
        table_disp.append(temp)

    chips = pygame.image.load("PNG-cards-1.3/chips.png")
    chips = pygame.transform.scale(chips, (100, 145))

    over1 = False
    over2 = False
    over3 = False
    over_d = False
    Raise = False
    Bet = False
    userinput = ''
    while end is False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = True
                game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if over_d:
                    end = True
                if over1:
                    if current_call > 0 and can_raise and current_call < player.get_chips(
                    ):
                        print("Raising")
                        Raise = True

                    if current_call <= 0 and player.get_chips() > 0:
                        print("Betting")
                        Bet = True

                if over2 and not Raise and not Bet:
                    if current_call > 0:
                        print("Calling")
                        if current_call > player.get_chips():
                            chip = player.get_chips()
                            player.remove_chips(chip)
                            table.add_chips(chip)
                        else:
                            player.remove_chips(current_call)
                            table.add_chips(current_call)
                        return -1

                    else:
                        print("Checking")
                        return 0

                if over3 and not Raise and not Bet:
                    print('Folding')
                    return 'Fold'

            if (Raise or Bet) and event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    userinput += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    userinput = userinput[:-1]
                elif event.key == pygame.K_RETURN:
                    converted_input = int(userinput)
                    if Raise:
                        if current_call + converted_input > player.get_chips():
                            userinput = ''
                        else:
                            player.remove_chips(converted_input + current_call)
                            table.add_chips(converted_input + current_call)
                            return converted_input
                    if Bet:
                        if converted_input > player.get_chips():
                            userinput = ''
                        else:
                            player.remove_chips(converted_input)
                            table.add_chips(converted_input)
                            return converted_input

        Window.blit(empty_table, (0, 0))
        Window.blit(first_card, (650, 500))
        Window.blit(second_card, (500, 500))
        if not done:
            Window.blit(facedown, (650, 100))
            Window.blit(facedown, (500, 100))
        if done:
            Window.blit(bot_first_card, (650, 100))
            Window.blit(bot_second_card, (500, 100))
        dx = 0
        for c in table_disp:
            Window.blit(c, (300 + dx, 300))
            dx += 150
        Window.blit(chips, (800, 450))
        Window.blit(chips, (800, 100))
        Window.blit(chips, (150, 250))
        myfont = pygame.font.SysFont("monospace", 25, bold=True)

        player_chips = myfont.render(
            "Player chips: " + str(player.get_chips()), 1, white)
        Window.blit(player_chips, (800, 460))

        bot_chips = myfont.render("Bot chips: " + str(bot.get_chips()), 1,
                                  white)
        Window.blit(bot_chips, (800, 200))

        table_chips = myfont.render("Table chips: " + str(table.get_chips()),
                                    1, white)
        Window.blit(table_chips, (200, 250))

        disp_cc = myfont.render("Current call: " + str(current_call), 1, white)
        Window.blit(disp_cc, (10, 10))

        position = pygame.mouse.get_pos()
        if not done:

            x1 = 20
            y1 = 500
            dx1 = 100
            dy1 = 50

            if position[0] >= x1 and position[0] <= x1 + dx1 and position[1] >= y1 and position[1] <= y1 + dy1:
                pygame.draw.rect(Window, grey, (x1, y1, dx1, dy1))
                over1 = True
            else:
                pygame.draw.rect(Window, white, (x1, y1, dx1, dy1))
                over1 = False

            if current_call > 0:
                b1 = myfont.render("Raise", 1, black)

            else:
                b1 = myfont.render("Bet", 1, black)

            Window.blit(b1, (x1 + dx1 / 6, y1 + dy1 / 6))

            x2 = 160
            y2 = 500
            dx2 = 100
            dy2 = 50

            if position[0] >= x2 and position[0] <= x2 + dx2 and position[1] >= y2 and position[1] <= y2 + dy2:
                pygame.draw.rect(Window, grey, (x2, y2, dx2, dy2))
                over2 = True
            else:
                pygame.draw.rect(Window, white, (x2, y2, dx2, dy2))
                over2 = False

            if current_call > 0:
                b2 = myfont.render("Call", 1, black)
            else:
                b2 = myfont.render("Check", 1, black)
            Window.blit(b2, (x2 + dx2 / 6, y2 + dy2 / 6))

            x3 = 300
            y3 = 500
            dx3 = 100
            dy3 = 50

            if position[0] >= x3 and position[0] <= x3 + dx3 and position[1] >= y3 and position[1] <= y3 + dy3:
                pygame.draw.rect(Window, grey, (x3, y3, dx3, dy3))
                over3 = True
            else:
                pygame.draw.rect(Window, white, (x3, y3, dx3, dy3))
                over3 = False

            b3 = myfont.render("Fold", 1, black)
            Window.blit(b3, (x3 + dx3 / 6, y3 + dy3 / 6))

            if Raise or Bet:
                quest = myfont.render("By how much?", 1, white)
                Window.blit(quest, (20, 600))
                ans = myfont.render(userinput, 1, white)
                Window.blit(ans, (220, 600))

        else:

            x = 150
            y = 600
            dx = 100
            dy = 50

            if player.get_chips() == 0:
                win = myfont.render("Bot is the winner!", 1, white)
                Window.blit(win, (10, 500))

            if bot.get_chips() == 0:
                win = myfont.render("Player is the winner!", 1, white)
                Window.blit(win, (10, 500))

            if position[0] >= x and position[0] <= x + dx and position[1] >= y and position[1] <= y + dy:
                pygame.draw.rect(Window, grey, (x, y, dx, dy))
                over_d = True
            else:
                pygame.draw.rect(Window, white, (x, y, dx, dy))
                over_d = False

            b_d = myfont.render("Done", 1, black)
            Window.blit(b_d, (x + dx / 4, y + dy / 4))

        pygame.display.update()
        clock.tick(60)  # fps


def get_file_name(card):
    """
    Given a card, this function produces a file_name so that we can draw the cards.

    Inputs: card - the card to be converted

    Outputs: The file name that cooresponds to the inputted card.

    Runtime: O(1)
    """
    start = str(card[0])
    if card[0] == 11:
        start = 'jack'
    if card[0] == 12:
        start = 'queen'
    if card[0] == 13:
        start = 'king'
    if card[0] == 14:
        start = 'ace'
    cardfilename = start + '_of_' + card[1].lower() + '.png'
    return cardfilename


def bet_call(player, bot, table):
    """
    This function handels the case where either the player or bot folds or
    goes all in.

    Inputs:
    player- an object of the player class
    bot - an object of the bot class, essentially our bot we will be playing against
    table - an object of the Table class

    Outputs:
    0 if there is no folding or all ins
    1 if someone goes all in
    2 if someone folds
    None - otherwise

    Runtime: N/A since dependent on user input
    """
    skip_to_end = 0
    d = bet(player, bot, table)  # Runtime dependent on user input
    if type(d) is tuple:
        if d[0] == 'All in':
            skip_to_end = 1
            return skip_to_end

        if type(d[1]) is Bot:
            table.give_pot(player)
        if type(d[1]) is Player:
            table.give_pot(bot)
        skip_to_end = 2
    print('p: ', player.get_chips(), 'b: ', bot.get_chips(), 't: ',
          table.get_chips())
    print('\n' * 3)
    return skip_to_end


def bet(player, bot, table):
    """
    For each round this function handells all the betting by letting the player
    bet and then the bot bet, the player and bot can keep betting and Raising and
    this loop ends if a player goes all in, folds, calls, or if both the bot and
    player check

    Inputs:
    player- an object of the player class
    bot - an object of the bot class, essentially our bot we will be playing against
    table - an object of the Table class

    Output:
    True - if the player or bot calls or if they both check
    (All in, Player) - if the player goes all in
    (All in, Bot) - if the bot goes all in
    (Fold, Player) - if the player folds
    (Fold, Bot) - if the bot folds

    Runtime: N/A since it depends on user input and the playstyle of the player
    and bot (if they bet or fold or etc..)

    """
    current_call = 0
    while True:
        print('Player turn')
        if bot.get_chips() == 0:
            current_call = player_bet(
                current_call, player, bot, table, can_raise=False)
            if game_over:
                pygame.quit()
                quit()
        else:
            current_call = player_bet(current_call, player, bot, table)
            if game_over:
                pygame.quit()
                quit()

        if current_call == -1:
            break

        print('p: ', player.get_chips(), 'b: ', bot.get_chips(), 't: ',
              table.get_chips())
        print('player current_call: ', current_call)

        if current_call is 'Fold':
            return (current_call, player)

        if player.get_chips() == 0:
            current_call = bot_bet(current_call, bot, table, can_raise=False)
        else:
            current_call = bot_bet(current_call, bot, table)

        print('p: ', player.get_chips(), 'b: ', bot.get_chips(), 't: ',
              table.get_chips())
        print('bot current_call: ', current_call)

        if current_call is 'Fold':
            return (current_call, bot)

        if current_call == 0 or current_call == -1:
            break

    if player.get_chips() == 0:
        return ('All in', player)
    if bot.get_chips() == 0:
        return ('All in', bot)
    return True


def setup():
    """
    Sets up the screen, and initializes the player, deck, bot and table objects

    Inputs: None

    Outputs:
    cards - an object of the Deck class
    table - an object of the Table class
    player- an object of the player class
    bot - an object of the bot class, essentially our bot we will be playing against

    Runtime: N/A since it is dependent on user input
    """
    start_screen()  # Runtime dependent on user input
    if game_over:
        pygame.quit()
        quit()
    cards = Deck()
    cards.shuffle()  # O(n)
    table = Table()
    player = Player('p')
    bot = Bot()
    return (cards, table, player, bot)


def end_of_round(cards, table, player, bot, skip):
    """
    This function handels what happens at the end of each round.

    Inputs:
    cards - an object of the Deck class
    table - an object of the Table class
    player- an object of the player class
    bot - an object of the bot class, essentially our bot we will be playing against
    skip - 2 if someone folded, therefore we do not need to calculate winner

    Outputs: None.

    Runtime: O(p*xlog(x) + plog(p)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table and p is the number of players (in our case 2 player and bot)
    """
    if skip == 2:
        print('skipping')
        return
    while len(table.get_cards()) < 5:  # essentially O(1)
        cards.push_to_table(table, 1)
    table.print_cards()
    player.print_cards()
    bot.print_cards()
    w = winner(table, [player, bot])  # O(p*xlog(x) + plog(p))
    print(w)
    if type(w) is Player:
        table.give_pot(player)
    if type(w) is Bot:
        table.give_pot(bot)
    print('p: ', player.get_chips(), 'b: ', bot.get_chips(), 't: ',
          table.get_chips())
    print('\n' * 5)


def main():
    """
    The main function, it calls setup to initialize everything then it calls
    rounds to handel all the different rounds, then calls end of round to handel
    the end of the rounds, finally calls player bet with the done flag turned on
    so the player can see if they won or lost that round.

    Inputs: None.

    Outputs: None.

    Runtime: N/A since it depends on user input and the playstyle of the player
    and bot (if they bet or fold or etc..)
    """
    cards, table, player, bot = setup()
    while True:
        skip = rounds(cards, table, player, bot)
        end_of_round(cards, table, player, bot, skip)
        player_bet(0, player, bot, table, done=True)
        if game_over or player.get_chips() <= 0 or bot.get_chips() <= 0:
            pygame.quit()
            quit()
        cards.collect([player, bot, table])


def rounds(cards, table, player, bot):
    """
    This funtion handels all the different rounds, it starts off when there is
    no cards on the table, then gives the user and the bot an ability to determine
    what to do and then repeates this for 3,4, and 5 cards on the table, unless
    the player or bot folds or goes all in, in that scenario this just skips to
    the end.

    Input:
    cards - an object of the Deck class
    table - an object of the Table class
    player- an object of the player class
    bot - an object of the bot class, essentially our bot we will be playing against

    Outputs:
    1 - if the player or bot goes all in
    2 - if the player or bot folds
    None - otherwise

    Runtime: N/A since it depends on user input and the playstyle of the player
    and bot (if they bet or fold or etc..)
    """
    global r  # the round number, only used for testing
    print("\n\n\nLET ROUND {} BEGIN!!!\n".format(r))
    r += 1
    print('p: ', player.get_chips(), 'b: ', bot.get_chips(), 't: ',
          table.get_chips())
    print('\n\n\n')
    cards.deal([player, bot], 2)
    player.print_cards()
    bot.print_cards()
    check = bet_call(player, bot, table)
    if check == 1 or check == 2:
        return check

    cards.push_to_table(table, 3)
    table.print_cards()
    check = bet_call(player, bot, table)
    if check == 1 or check == 2:
        return check

    cards.push_to_table(table, 1)
    table.print_cards()
    check = bet_call(player, bot, table)
    if check == 1 or check == 2:
        return check

    cards.push_to_table(table, 1)
    table.print_cards()
    check = bet_call(player, bot, table)
    if check == 1 or check == 2:
        return check


if __name__ == '__main__':

    # Determines whether or not to use the profiler based off of the parser args.
    if args.profiler:
        cProfile.run('main()')
    else:
        main()
