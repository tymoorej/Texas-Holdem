"""
This file handels all of the betting that the bot does.
"""

from winning_hand import winner
import itertools
from card import *
from random import *

MONTE_CARLO_ITERATIONS = 10000


def bot_bet(current_call, bot, table, can_raise=True):
    """
    Handelling of the betting done by the bot. This function calls on our
    Monte Carlo algorithm to determine the probability of the bot winning, Then
    based off the probability and some random chance we determine whether or not
    to either raise, bet, call, check, or fold. If the bot raises or bets then
    how much chips it puts in is proportional to its chance of winning the round.

    Inputs:
    current call - the minimum amount of chips the bot must put in.
    bot - an object of the bot class, essentially our bot we will be playing against
    table - an object of the Table class
    can_raise=True - whether or not the bot is allowed to raise, default is True


    Output: The call the player must make, or 'Fold' if the bot folds.

    Runtime: O(p*xlog(x) + plog(p)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table and p is the number of players
    """
    print('bot turn: ', end=' ')
    chance = Monte_Carlo(bot, table)  # O(p*xlog(x) + plog(p))
    chance = chance // 100  # chance=(chance/10,000)*100%
    print("Chance BEFORE: ", chance)
    chance = chance + randint(-15, 15)  # gives the bot a bit of randomness
    if chance <= 0:
        chance = 0
    if chance >= 100:
        chance = 100
    print("Chance AFTER:   ", chance)

    if type(current_call) is int and current_call > 0:
        if chance >= 50 and bot.get_chips(
        ) - current_call > 0 and can_raise is True:
            base = (chance - 50) / 50
            value = int(base * (bot.get_chips() - current_call))
            print('Raising by: ', value)
            bot.remove_chips(value + current_call)  #O(n)
            table.add_chips(value + current_call)  #O(m)
            return value

        if chance >= 50 and (bot.get_chips() - current_call <= 0
                             or can_raise is False):
            print('calling')
            chip = min(current_call, bot.get_chips())
            bot.remove_chips(chip)  #O(n)
            table.add_chips(chip)  #O(m)
            return -1

        if chance >= 30 and chance < 50:
            print('calling')
            if current_call > bot.get_chips():
                print('Bot goes all in')
                chip = bot.get_chips()
                bot.remove_chips(chip)  #O(n)
                table.add_chips(chip)  #O(m)
                return -1
            else:
                bot.remove_chips(current_call)  #O(n)
                table.add_chips(current_call)  #O(m)
                return -1
        if chance < 30:
            print('folding')
            return 'Fold'
    else:
        if chance >= 50:
            base = (chance - 50) / 50
            value = int(base * bot.get_chips())
            print('betting by', value)
            bot.remove_chips(value)  #O(n)
            table.add_chips(value)  #O(m)
            return value

        else:
            print('checking')
            return 0


def Monte_Carlo(bot, table):
    """
    A implimentation of the Monte Carlo algorithm, this algorithm works by taking
    a sample size of the different possibilities of what the remaining cards on the
    table will be and what cards the player has in their hand. It takes 10,000
    different samples and calculates if it will win in each scenario and returns
    how many times it won out of 10,000

    Inputs:
    bot - an object of the bot class, essentially our bot we will be playing against
    table - an object of the Table class

    Output: How many times the bot won in 10,000 scenarios

    Runtime: O(p*xlog(x) + plog(p)) where x=n+m where n is the the number of cards that the player
    has and m is the number of cards on the table and p is the number of players
    """
    count = 0
    for i in range(MONTE_CARLO_ITERATIONS):  #O(10,000)=O(1)
        my_deck = Deck()
        my_deck.remove_card(bot.get_cards()[0])  #O(n)
        my_deck.remove_card(bot.get_cards()[1])  #O(n)

        # for card in table.get_cards():
        #     my_deck.remove_card(card)

        listed_deck = my_deck.get_cards()
        x = sample(listed_deck, 7 - len(table.get_cards()))
        person = Player(0, x[0:2])
        players = [person, bot]
        table2 = Table(table.get_cards() + x[2:])

        if type(winner(table2, players,
                       printing=False)) is Bot:  #O(p*xlog(x) + plog(p))
            count += 1

    return count
