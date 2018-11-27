import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import winning_hand
from card import Player
from card import Table


class WinningHandTestCase(unittest.TestCase):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    NO_HAND = 1

    @staticmethod
    def issue_cards(player, cards):
        for card in cards:
            player.add_card(card)

    def setUp(self):
        self.player1 = Player('p1')
        self.player2 = Player('p2')
        self.table = Table()

    def test_printable_dict_of_winners(self):
        # TODO: Implementation
        pass

    def test_winner_player1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Clubs'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(self.player2, [(4, 'Hearts'), (8, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertEqual(self.player1, winning_hand.winner(self.table, [self.player1, self.player2], printing=False))

    def test_winner_player2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Clubs'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(self.player2, [(4, 'Hearts'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertEqual(self.player2, winning_hand.winner(self.table, [self.player1, self.player2], printing=False))

    def test_get_value_royal_flush(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(10, 'Spades'), (11, 'Spades'), (12, 'Spades'), (13, 'Spades'), (4, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.ROYAL_FLUSH, self.player1.get_hand())

    def test_get_value_straight_flush(self):

        WinningHandTestCase.issue_cards(self.player1, [(9, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Spades'), (6, 'Spades'), (7, 'Spades'), (8, 'Spades'), (4, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.STRAIGHT_FLUSH, self.player1.get_hand())

    def test_get_value_four_of_a_kind(self):

        WinningHandTestCase.issue_cards(self.player1, [(4, 'Hearts'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (4, 'Clubs'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.FOUR_OF_A_KIND, self.player1.get_hand())

    def test_get_value_full_house(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (4, 'Hearts')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (2, 'Clubs')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.FULL_HOUSE, self.player1.get_hand())

    def test_get_value_flush(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Spades'), (12, 'Spades')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.FLUSH, self.player1.get_hand())

    def test_get_value_straight(self):

        WinningHandTestCase.issue_cards(self.player1, [(3, 'Clubs'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.STRAIGHT, self.player1.get_hand())

    def test_get_value_three_of_a_kind(self):

        WinningHandTestCase.issue_cards(self.player1, [(6, 'Clubs'), (6, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.THREE_OF_A_KIND, self.player1.get_hand())

    def test_get_value_two_pair(self):

        WinningHandTestCase.issue_cards(self.player1, [(4, 'Hearts'), (5, 'Hearts')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.TWO_PAIR, self.player1.get_hand())

    def test_get_value_one_pair(self):

        WinningHandTestCase.issue_cards(self.player1, [(4, 'Hearts'), (10, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.ONE_PAIR, self.player1.get_hand())

    def test_get_value_no_hand(self):

        WinningHandTestCase.issue_cards(self.player1, [(9, 'Clubs'), (10, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        winning_hand.get_value(self.table, self.player1)

        self.assertEqual(WinningHandTestCase.NO_HAND, self.player1.get_hand())

    def test_has_royal_flush(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Spades'), (13, 'Spades')])
        WinningHandTestCase.issue_cards(self.table, [(10, 'Spades'), (11, 'Spades'), (12, 'Spades')])

        self.assertTrue(winning_hand.has_royal_flush(self.table, self.player1))

    def test_if_straight_flush1(self):

        straight = [5, 6, 7, 8, 9]
        WinningHandTestCase.issue_cards(self.player1, [(9, 'Spades'), (2, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Spades'), (6, 'Spades'), (7, 'Spades'), (8, 'Spades'), (4, 'Hearts')])

        self.assertTrue(winning_hand.if_straight_is_flush(straight, self.table, self.player1))

    def test_if_straight_flush2(self):

        straight = [5, 6, 7, 8, 9]
        WinningHandTestCase.issue_cards(self.player1, [(9, 'Diamonds'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Diamonds'), (6, 'Diamonds'), (7, 'Diamonds'), (8, 'Diamonds'), (11, 'Clubs')])

        self.assertTrue(winning_hand.if_straight_is_flush(straight, self.table, self.player1))

    def test_if_straight_flush3(self):

        straight = [5, 6, 7, 8, 9]
        WinningHandTestCase.issue_cards(self.player1, [(9, 'Hearts'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Hearts'), (6, 'Hearts'), (7, 'Hearts'), (8, 'Hearts'), (11, 'Clubs')])

        self.assertTrue(winning_hand.if_straight_is_flush(straight, self.table, self.player1))

    def test_if_straight_flush4(self):

        straight = [5, 6, 7, 8, 9]
        WinningHandTestCase.issue_cards(self.player1, [(9, 'Clubs'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Clubs'), (6, 'Clubs'), (7, 'Clubs'), (8, 'Hearts'), (11, 'Diamonds')])

        self.assertFalse(winning_hand.if_straight_is_flush(straight, self.table, self.player1))

    def test_has_straight_flush1(self):

        WinningHandTestCase.issue_cards(self.player1, [(9, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Spades'), (6, 'Spades'), (7, 'Spades'), (8, 'Spades'), (4, 'Hearts')])

        self.assertTrue(winning_hand.has_straight_flush(self.table, self.player1))

    def test_has_straight_flush2(self):

        WinningHandTestCase.issue_cards(self.player1, [(9, 'Diamonds'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Spades'), (6, 'Spades'), (7, 'Spades'), (8, 'Spades'), (4, 'Hearts')])

        self.assertFalse(winning_hand.has_straight_flush(self.table, self.player1))

    def test_has_straight_flush3(self):

        WinningHandTestCase.issue_cards(self.player1, [(9, 'Diamonds'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(5, 'Spades'), (6, 'Spades'), (7, 'Spades'), (11, 'Spades'), (4, 'Hearts')])

        self.assertFalse(winning_hand.has_straight_flush(self.table, self.player1))

    def test_has_four_of_a_kind1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(2, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_four_of_a_kind(self.table, self.player1))

    def test_has_four_of_a_kind2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(3, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertFalse(winning_hand.has_four_of_a_kind(self.table, self.player1))

    def test_has_full_house1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (4, 'Hearts')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (2, 'Clubs')])

        self.assertTrue(winning_hand.has_full_house(self.table, self.player1))

    def test_has_full_house2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (10, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (2, 'Clubs')])

        self.assertFalse(winning_hand.has_full_house(self.table, self.player1))

    def test_has_flush1(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Spades'), (12, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Spades'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_flush(self.table, self.player1))

    def test_has_flush2(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Hearts'), (12, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Clubs'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertFalse(winning_hand.has_full_house(self.table, self.player1))

    def test_has_straight1(self):

        WinningHandTestCase.issue_cards(self.player1, [(3, 'Clubs'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_straight(self.table, self.player1))

    def test_has_straight2(self):

        WinningHandTestCase.issue_cards(self.player1, [(14, 'Clubs'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertFalse(winning_hand.has_straight(self.table, self.player1))

    def test_has_three_of_a_kind1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_three_of_a_kind(self.table, self.player1))

    def test_has_three_of_a_kind2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (11, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertFalse(winning_hand.has_three_of_a_kind(self.table, self.player1))

    def test_has_two_pair1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (4, 'Diamonds')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_two_pair(self.table, self.player1))

    def test_has_two_pair2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (7, 'Clubs')])
        WinningHandTestCase.issue_cards(self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds')])

        self.assertFalse(winning_hand.has_two_pair(self.table, self.player1))

    def test_has_one_pair1(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (7, 'Clubs')])
        WinningHandTestCase.issue_cards(
            self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades'), (2, 'Diamonds'), (8, 'Hearts')])

        self.assertTrue(winning_hand.has_one_pair(self.table, self.player1))

    def test_has_one_pair2(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (7, 'Clubs')])
        WinningHandTestCase.issue_cards(self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades')])

        self.assertFalse(winning_hand.has_one_pair(self.table, self.player1))

    def test_repeated_cards(self):
        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (2, 'Clubs')])
        WinningHandTestCase.issue_cards(self.table, [(4, 'Spades'), (5, 'Spades'), (6, 'Spades')])

        card_freq = {2: 2, 4: 1, 5: 1, 6: 1}
        repeated_cards = winning_hand.repeated_cards(self.table, self.player1)

        self.assertEqual(len(card_freq), len(repeated_cards))

        for card, freq in card_freq.items():
            self.assertTrue(card in repeated_cards)
            self.assertEqual(freq, repeated_cards[card])

    def test_highest_card(self):

        WinningHandTestCase.issue_cards(self.player1, [(2, 'Spades'), (7, 'Clubs')])

        expected_players = [self.player1]
        actual_players = winning_hand.highest_card([self.player1])

        for expected, actual in zip(expected_players, actual_players):
            self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
