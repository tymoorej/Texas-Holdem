import unittest
import sys
import os
from .test_utils import StdoutCapture

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from card import Deck
from card import Table
from card import Player


class DeckTestCase(unittest.TestCase):

    def setUp(self):
        self.full_deck = Deck()
        self.empty_deck = Deck()

        while len(self.empty_deck.get_cards()) > 0:
            self.empty_deck.remove_random_card()

    @staticmethod
    def generateFullDeck():
        cards = []
        for val in range(2, 15):
            for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
                cards.append((val, suit))

        return cards

    @staticmethod
    def sortBySuit(cards):
        cards.sort(key=lambda card: (card[1], card[0]))

    @staticmethod
    def equalCards(cards1, cards2, after_sort=True):
        if len(cards1) != len(cards2):
            return False

        if after_sort:
            DeckTestCase.sortBySuit(cards1)
            DeckTestCase.sortBySuit(cards2)

        for i, card in enumerate(cards1):
            if card[0] != cards2[i][0] or card[1] != cards2[i][1]:
                return False

        return True

    def test_initializer(self):
        deck = Deck()
        self.assertEqual(52, len(deck.get_cards()))

    def test_print_cards(self):
        cards = DeckTestCase.generateFullDeck()

        _, output = StdoutCapture(lambda : self.full_deck.print_cards()).capture()

        self.assertTrue(str(52) in output)
        self.assertTrue(str(cards) in output)

    def test_get_cards(self):
        all_cards = DeckTestCase.generateFullDeck()
        cards = self.full_deck.get_cards()

        self.assertTrue(DeckTestCase.equalCards(all_cards, cards))

    def test_shuffle(self):
        old_cards = self.full_deck.get_cards().copy()
        self.full_deck.shuffle()

        new_cards = self.full_deck.get_cards()
        self.assertFalse(DeckTestCase.equalCards(old_cards, new_cards, after_sort=False))

    def test_remove_random_card_exists(self):
        cards = self.full_deck.get_cards().copy()
        card = self.full_deck.remove_random_card()

        self.assertTrue(card in cards)
        self.assertFalse(card in self.full_deck.get_cards())

    def test_remove_random_card_nonexistent(self):
        card, output = StdoutCapture(lambda: self.empty_deck.remove_random_card()).capture()

        self.assertEqual(card, None)
        self.assertEqual("Deck is empty", output.strip())

    def test_remove_top_card_exists(self):
        cards = self.full_deck.get_cards().copy()
        card = self.full_deck.remove_top_card()

        self.assertEqual(card, cards[0])
        self.assertFalse(card in self.full_deck.get_cards())

    def test_remove_top_card_nonexistent(self):
        card, output = StdoutCapture(lambda: self.empty_deck.remove_top_card()).capture()

        self.assertEqual(card, None)
        self.assertEqual("Deck is empty", output.strip())

    def test_remove_card_exists(self):
        target_card = (2, "Spades")
        self.assertTrue(target_card in self.full_deck.get_cards())

        self.full_deck.remove_card(target_card)
        self.assertFalse(target_card in self.full_deck.get_cards())

    def test_remove_card_nonexistent(self):
        card, output = StdoutCapture(lambda: self.empty_deck.remove_card((2, "Spades"))).capture()

        self.assertEqual(card, None)
        self.assertEqual("Deck is empty", output.strip())

    def test_deal(self):
        player1 = Player("p1")
        player2 = Player("p2")

        self.assertEqual(52, len(self.full_deck.get_cards()))
        self.assertEqual(0, len(player1.get_cards()))
        self.assertEqual(0, len(player2.get_cards()))

        self.full_deck.deal([player1, player2], 2)

        self.assertEqual(48, len(self.full_deck.get_cards()))
        self.assertEqual(2, len(player1.get_cards()))
        self.assertEqual(2, len(player2.get_cards()))

    def test_collect(self):
        player1 = Player("p1")
        player2 = Player("p2")

        player1_cards = [(2, "Spades"), (2, "Hearts")]
        player2_cards = [(4, "Hearts")]

        for card in player1_cards:
            player1.add_card(card)

        for card in player2_cards:
            player2.add_card(card)

        self.assertEqual(0, len(self.empty_deck.get_cards()))
        self.assertEqual(2, len(player1.get_cards()))
        self.assertEqual(1, len(player2.get_cards()))

        self.empty_deck.collect([player1, player2])

        self.assertEqual(3, len(self.empty_deck.get_cards()))

        for card in player1_cards:
            self.assertTrue(card in self.empty_deck.get_cards())

        for card in player2_cards:
            self.assertTrue(card in self.empty_deck.get_cards())

    def test_have_all_cards(self):
        full_deck = Deck()

        self.assertTrue(full_deck.have_all_cards())
        full_deck.remove_random_card()
        self.assertFalse(full_deck.have_all_cards())

    def test_push_to_table(self):
        table = Table()

        self.assertEqual(0, len(table.get_cards()))
        self.assertEqual(52, len(self.full_deck.get_cards()))

        self.full_deck.push_to_table(table, 3)

        self.assertEqual(3, len(table.get_cards()))
        self.assertEqual(49, len(self.full_deck.get_cards()))


    def test_print(self):
        _, output = StdoutCapture(lambda: print(self.empty_deck)).capture()
        self.assertEqual("Deck of cards", output.strip())


if __name__ == '__main__':
    unittest.main()
