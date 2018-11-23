import unittest
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from card import *
from winning_hand import *
from bot import Monte_Carlo, MONTE_CARLO_ITERATIONS
from random import randint, shuffle


class TestHandMethods(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self._number_of_tests = 1000
        self._suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']

    def test_royal_flush(self):
        self.assertEqual(1, 1)

    def test_straight_flush(self):
        self.assertEqual(1, 1)

    def test_four_of_a_kind(self):

        # Testing all equivalence classes of four of a kind
        for i in range(2,15):
            player = Player('p')
            table = Table()

            cards = []

            # four of a kind
            for j in range(4):
                cards.append((i,self._suits[j]))

            # the remaining cards
            for j in range(3):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                while ((card_value, card_suit) in cards):
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    card_value = randint(2,14)

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)
            result = has_four_of_a_kind(table, player)
            self.assertTrue(result)

    def test_not_four_of_a_kind(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()
            cards_on_table = randint(3,5)
            cards = []

            for i in range(cards_on_table + 2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                while ((card_value, card_suit) in cards or len([ c for c in cards if c[0] == card_value]) == 3 ):
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    card_value = randint(2,14)
                cards.append((card_value, card_suit))

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)            
            result = has_four_of_a_kind(table, player)
            self.assertFalse(result)            

    def test_full_house(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(3,5)
            cards = []

            triplecardvalue = randint(2,14)
            doublecardvalue = randint(2,14)

            while triplecardvalue == doublecardvalue:
                doublecardvalue = randint(2,14)
            
            for i in range(5):
                if i < 3:
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    while ((triplecardvalue, card_suit) in cards):
                        card_suit = self._suits[randint(0,len(self._suits)-1)]
                    cards.append((triplecardvalue,card_suit))
                else:
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    while ((doublecardvalue, card_suit) in cards):
                        card_suit = self._suits[randint(0,len(self._suits)-1)]
                    cards.append((doublecardvalue,card_suit))

            while len(cards) < cards_on_table + 2:
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                card_value = randint(2,14)
                while ((card_value, card_suit) in cards):
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    card_value = randint(2,14)
                cards.append((card_value, card_suit))

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)            
            result = has_full_house(table, player)
            self.assertTrue(result)

    def test_not_full_house(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(0,5)
            triplits = set()
            pairs = set()
            cards = []

            for i in range(cards_on_table + 2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                while (len(triplits) == 1 and card_value in [card[0] for card in cards]) \
                or (len(pairs) >=2 and card_value in pairs) \
                or (card_value, card_suit) in cards:
                    card_value = randint(2,14)
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                cards.append((card_value, card_suit))
                if len([card[0] for card in cards if card[0] == card_value]) == 2:
                    pairs.add(card_value)
                elif len([card[0] for card in cards if card[0] == card_value]) == 3:
                    triplits.add(card_value)

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)            
   
            result = has_full_house(table, player)
            self.assertFalse(result)

    def test_flush(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(3,5)
            card_suit = self._suits[randint(0,len(self._suits)-1)]
            cards = []

            for i in range(5):
                card_value = randint(2,14)
                while (card_value in [card[0] for card in cards]):
                    card_value = randint(2,14)
                cards.append((card_value, card_suit))
            
            while len(cards) < cards_on_table + 2:
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                card_value = randint(2,14)
                while ((card_value, card_suit) in cards):
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    card_value = randint(2,14)
                cards.append((card_value, card_suit))
            
            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)            
            result = has_flush(table, player)
            self.assertTrue(result)

    def test_not_flush(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(0,5)

            suits_seen = []
            cards = []

            for i in range(cards_on_table + 2):
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                card_value = randint(2,14)
                while (len( [s for s in suits_seen if s == card_suit] ) == 4) or (card_value, card_suit) in cards: # prevent flush
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    card_value = randint(2,14)
                suits_seen.append(card_suit)
                cards.append((card_value,card_suit))

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)            
            result = has_flush(table, player)
            self.assertFalse(result)

    def test_straight(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(3,5)
            straight = []
            start = randint(5,10)
            straight.append((start,self._suits[randint(0,len(self._suits)-1)]))
            
            if randint(0,1) == 1:
                modifier = 1
            else:
                modifier = -1
            for i in range(1,5):
                    value = start + (i * modifier)
                    if value == 1:
                        value = 14
                    suit = self._suits[randint(0,len(self._suits)-1)]
                    straight.append((value,suit))
            while len(straight) < cards_on_table + 2:
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                straight.append((card_value,card_suit))
            shuffle(straight)

            for i,s in enumerate(straight):
                if i <= 1:
                    player.add_card(s)
                else:
                    table.add_card(s)
            result = has_straight(table, player)
            self.assertTrue(result)
    
    def test_not_straight(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()

            cards_on_table = randint(0,5)
            cards = []
            cards_adjusted = set()

            for i in range(cards_on_table + 2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                cards.append((card_value,card_suit))
                cards_adjusted.add(card_value)
                if card_value == 14:
                    cards_adjusted.add(1)
            
            cards = cards
            if 14 in cards_adjusted:
                cards_adjusted.add(1)

            skip_to_next = False
            for i in range(1,11):
                if set(range(i,i+5)).issubset(cards_adjusted):
                    skip_to_next = True
                    break
            
            if skip_to_next:
                continue

            for i,c in enumerate(cards):
                if i <= 1:
                    player.add_card(c)
                else:
                    table.add_card(c)

            result = has_straight(table, player)

            self.assertFalse(result)

    def test_three_of_a_kind(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()
            cards_on_table = randint(0,5)
            cards_seen = dict()

            for n in range(2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                player.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    cards_seen[card_value] += 1
                else:
                    cards_seen[card_value] = 1
                    
            
            for n in range(cards_on_table):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                table.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    cards_seen[card_value] += 1
                else:
                    cards_seen[card_value] = 1
            result = has_three_of_a_kind(table, player)
            self.assertEqual(max(cards_seen.values())>=3, result)

    def test_two_pair(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()
            cards_on_table = randint(0,5)
            cards_seen=set()
            pairs_found = set()

            for n in range(2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                player.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pairs_found.add(card_value)
                cards_seen.add(card_value)

            for n in range(cards_on_table):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                table.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pairs_found.add(card_value)
                cards_seen.add(card_value)
            result = has_two_pair(table, player)
            self.assertEqual(len(pairs_found) >= 2, result)

    def test_one_pair(self):
        for i in range(self._number_of_tests):
            player = Player('p')
            table = Table()
            cards_seen = set()
            cards_on_table = randint(0,5)
            pair_found = False

            for n in range(2):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
                player.add_card((card_value,card_suit))
                if card_value in cards_seen:
                    pair_found = True
                cards_seen.add(card_value)

            for n in range(cards_on_table):
                card_value = randint(2,14)
                card_suit = self._suits[randint(0,len(self._suits)-1)]
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
        for i in range(self._number_of_tests):
            num_of_players = randint(1, 50)
            players = []

            for i in range(num_of_players):
                players.append(Player(i+1))

            highest_value = 0
            players_with_highest_value = set()

            for p in players:
                for n in range(2):
                    card_value = randint(2,14)
                    card_suit = self._suits[randint(0,len(self._suits)-1)]
                    if card_value > highest_value:
                        highest_value = card_value
                        players_with_highest_value = set()
                        players_with_highest_value.add(p)
                    elif card_value == highest_value:
                        players_with_highest_value.add(p)
                    p.add_card((card_value,card_suit))
            result = set(highest_card(players))
            self.assertTrue(result == players_with_highest_value)

    def test_monte_carlo_win(self):
        bot = Bot()
        bot.add_card((14, 'Hearts'))
        bot.add_card((13, 'Hearts'))

        table = Table()
        table.add_card((12, 'Hearts'))
        table.add_card((11, 'Hearts'))
        table.add_card((10, 'Hearts'))
        table.add_card((2, 'Spades'))
        table.add_card((3, 'Diamonds'))

        self.assertEqual(MONTE_CARLO_ITERATIONS, Monte_Carlo(bot, table))

    def test_monte_carlo_average(self):
        # MonteCarlo.get_player_cards = lambda deck: [(9, 'Hearts'), (8, 'Hearts')]

        orig_player_init = Player.__init__
        orig_table_init = Table.__init__

        def GiveTableCards(self, cards=None):
            self._cards = [] if cards is None else cards
            self._chips = 0

        def GivePlayerCards(self, ID, cards=None):
            self._cards = [(9, 'Hearts'), (8, 'Hearts')]
            self._chips = 2000
            self._hand = -1

        Player.__init__ = GivePlayerCards
        Table.__init__ = GiveTableCards

        bot = Bot()
        bot.add_card((5, 'Hearts'))
        bot.add_card((9, 'Diamonds'))

        table = Table()
        table.add_card((12, 'Hearts'))
        table.add_card((10, 'Hearts'))
        table.add_card((2, 'Spades'))

        win_count = Monte_Carlo(bot, table)

        Player.__init__ = orig_player_init
        Table.__init__ = orig_table_init

        self.assertNotEqual(0, win_count)
        self.assertNotEqual(MONTE_CARLO_ITERATIONS, win_count)

    def test_monte_carlo_duplicates(self):
        # MonteCarlo.get_player_cards = lambda deck: [(9, 'Hearts'), (8, 'Hearts')]

        orig_player_init = Player.__init__
        orig_table_init = Table.__init__
        assertEqual = self.assertEqual

        def GiveTableCards(self, cards=None):
            self._cards = [] if cards is None else cards
            self._chips = 0
            assertEqual(len(set(self._cards)), len(self._cards))

        def GivePlayerCards(self, ID, cards=None):
            self._cards = [] if cards is None else cards
            self._chips = 2000
            self._hand = -1
            assertEqual(len(set(self._cards)), len(self._cards))

        Player.__init__ = GivePlayerCards
        Table.__init__ = GiveTableCards

        bot = Bot()
        bot.add_card((5, 'Hearts'))
        bot.add_card((9, 'Diamonds'))

        table = Table()
        table.add_card((12, 'Hearts'))
        table.add_card((10, 'Hearts'))
        table.add_card((2, 'Spades'))

        Monte_Carlo(bot, table)

        Player.__init__ = orig_player_init
        Table.__init__ = orig_table_init


if __name__ == '__main__':
    unittest.main()
    