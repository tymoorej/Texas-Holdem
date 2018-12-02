import unittest
import sys
import os
from .test_utils import StdoutCapture

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from card import Player
from card import Table


class TableTestCase(unittest.TestCase):

    def setUp(self):
        self.table = Table()

    @staticmethod
    def generate_full_deck():
        cards = []
        for val in range(2, 15):
            for suit in ["Hearts", "Diamonds", "Spades", "Clubs"]:
                cards.append((val, suit))

        return cards

    def test_initializer(self):
        empty_table = Table()
        self.assertEqual(0, empty_table.get_chips())
        self.assertEqual(0, len(empty_table.get_cards()))

        full_table = Table(TableTestCase.generate_full_deck())
        self.assertEqual(len(TableTestCase.generate_full_deck()), len(full_table.get_cards()))

    def test_give_pot(self):
        table_chips = 5000
        player1 = Player("p1")
        starting_chips = player1.get_chips()

        self.assertEqual(0, self.table.get_chips())
        self.table.add_chips(table_chips)

        self.table.give_pot(player1)
        self.assertEqual(table_chips+starting_chips, player1.get_chips())

    def test_print(self):
        _, output = StdoutCapture(lambda: print(self.table)).capture()
        self.assertEqual("Table", output.strip())


if __name__ == '__main__':
    unittest.main()
