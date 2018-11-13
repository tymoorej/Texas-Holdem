import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from card import *
from winning_hand import *
from random import randint

number_of_tests = 1000

class TestHandMethods(unittest.TestCase):

    def test_royal_flush(self):
        self.assertEqual(1, 1)

    def test_straight_flush(self):
        self.assertEqual(1, 1)

    def test_four_of_a_kind(self):
        self.assertEqual(1, 1)

    def test_full_house(self):
        self.assertEqual(1, 1)

    def test_flush(self):
        self.assertEqual(1, 1)

    def test_straight(self):
        self.assertEqual(1, 1)

    def test_three_of_a_kind(self):
        self.assertEqual(1, 1)

    def test_two_pair(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        for i in range(number_of_tests):
            player = Player('p')
            table = Table()
            cards_on_table = randint(0,5)
            cards_seen=set()
            pairs_found = set()

            for n in range(2):
                card_value = randint(2,14)
                card_suit = suits[randint(0,len(suits)-1)]
                player.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pairs_found.add(card_value)
                cards_seen.add(card_value)

            for n in range(cards_on_table):
                card_value = randint(2,14)
                card_suit = suits[randint(0,len(suits)-1)]
                table.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pairs_found.add(card_value)
                cards_seen.add(card_value)
            result = has_two_pair(table, player)
            self.assertEqual(len(pairs_found) >= 2, result)


    def test_one_pair(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        for i in range(number_of_tests):
            player = Player('p')
            table = Table()
            cards_seen = set()
            cards_on_table = randint(0,5)
            pair_found = False

            for n in range(2):
                card_value = randint(2,14)
                card_suit = suits[randint(0,len(suits)-1)]
                player.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pair_found = True
                cards_seen.add(card_value)

            for n in range(cards_on_table):
                card_value = randint(2,14)
                card_suit = suits[randint(0,len(suits)-1)]
                table.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pair_found = True
                cards_seen.add(card_value)
            result = has_one_pair(table, player)
            self.assertEqual(pair_found, result)

        self.assertEqual(1, 1)

    def test_repeated_cards(self):
        self.assertEqual(1, 1)

    def test_highest_card(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        for i in range(number_of_tests):
            num_of_players = randint(1, 50)
            players = []

            for i in range(num_of_players):
                players.append(Player(i+1))

            highest_value = 0
            players_with_highest_value = set()

            for p in players:
                for n in range(2):
                    card_value = randint(2,14)
                    card_suit = suits[randint(0,len(suits)-1)]
                    if card_value > highest_value:
                        highest_value = card_value
                        players_with_highest_value = set()
                        players_with_highest_value.add(p)
                    elif card_value == highest_value:
                        players_with_highest_value.add(p)
                    p.add_card((card_value,card_suit))
            result = set(highest_card(players))
            self.assertTrue(result == players_with_highest_value)


if __name__ == '__main__':
    unittest.main()
    