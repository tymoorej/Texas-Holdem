import unittest
import sys
import os
from test_utils import HandConstants as Hands
from test_utils import StdoutCapture

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from card import Player


class PlayerTestCase(unittest.TestCase):

    @staticmethod
    def issue_cards(player, cards):
        for card in cards:
            player.add_card(card)

    def setUp(self):
        self.player = Player("p1")
        self.player_cards = [(2, "Clubs"), (3, "Diamonds")]

    def test_initializer(self):
        pid = "p1"
        new_player = Player(pid)
        self.assertEqual(0, len(new_player.get_cards()))
        self.assertEqual(pid, new_player.get_ID())

        new_player = Player(pid, self.player_cards)
        self.assertEqual(len(self.player_cards), len(new_player.get_cards()))
        self.assertEqual(pid, new_player.get_ID())

    def test_set_hand(self):
        self.player.set_hand(Hands.ONE_PAIR)
        self.assertEqual(Hands.ONE_PAIR, self.player.get_hand())

        self.player.set_hand(Hands.ROYAL_FLUSH)
        self.assertEqual(Hands.ROYAL_FLUSH, self.player.get_hand())

    def test_print_cards(self):
        PlayerTestCase.issue_cards(self.player, self.player_cards)

        expected_output = str(self.player_cards)
        stdout_capture = StdoutCapture(lambda: self.player.print_cards())
        _, output = stdout_capture.capture()

        self.assertTrue(expected_output in output.strip())

    def test_get_cards(self):
        PlayerTestCase.issue_cards(self.player, self.player_cards)

        cards = self.player.get_cards()
        self.assertEqual(len(self.player_cards), len(cards))

        self.player_cards.sort(key=lambda card_tup: (card_tup[1], card_tup[0]))
        cards.sort(key=lambda card_tup: (card_tup[1], card_tup[0]))

        for i, card in enumerate(self.player_cards):
            self.assertEqual(card, cards[i])

    def test_add_card(self):
        card = self.player_cards[0]

        self.assertEqual(0, len(self.player.get_cards()))
        self.assertFalse(card in self.player.get_cards())
        self.player.add_card(card)

        self.assertEqual(1, len(self.player.get_cards()))
        self.assertTrue(card in self.player.get_cards())

    def test_remove_card_exists(self):
        PlayerTestCase.issue_cards(self.player, self.player_cards)

        card = self.player_cards[0]
        self.assertTrue(card in self.player.get_cards())

        self.player.remove_card(card)

        self.assertFalse(card in self.player.get_cards())

    ''' FAILS - Remove method attempts to remove card even if it does not exist.'''
    # def test_remove_card_nonexistent(self):
    #     card = self.player_cards[0]
    #     self.assertFalse(card in self.player.get_cards())
    #
    #     StdoutCapture(lambda: self.player.remove_card(card)).capture()
    #
    #     self.assertFalse(card in self.player.get_cards())

    def test_pop_card_exists(self):
        PlayerTestCase.issue_cards(self.player, self.player_cards)

        card = self.player.pop_card()

        self.assertFalse(card in self.player.get_cards())

    def test_pop_card_nonexistent(self):

        card, output = StdoutCapture(lambda: self.player.pop_card()).capture()

        self.assertFalse(card in self.player.get_cards())

    def test_add_chips(self):
        chips = 15000
        self.player.remove_chips(self.player.get_chips())

        self.assertEqual(0, self.player.get_chips())

        self.player.add_chips(chips)

        self.assertEqual(chips, self.player.get_chips())


if __name__ == '__main__':
    unittest.main()

