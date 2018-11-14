import unittest
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from card import Table


class TableTestCase(unittest.TestCase):

    def setUp(self):
        self.table_cards = [
            (12, 'Spades'),
            (11, 'Hearts'),
            (2, 'Spades'),
            (7, 'Hearts'),
            (10, 'Diamonds')
        ]

    def test_constructs(self):
        table = Table()
        self.assertEqual(0, len(table.get_cards()))
        self.assertEqual(0, table.get_chips())

        table = Table(self.table_cards)
        self.assertEqual(len(self.table_cards), len(table.get_cards()))
        self.assertEqual(0, table.get_chips())


if __name__ == '__main__':
    unittest.main()
