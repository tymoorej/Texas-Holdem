import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from card import *
from bot import Monte_Carlo, MONTE_CARLO_ITERATIONS


class ExampleTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_example(self):
        self.assertTrue(True)

    def test_monte_carlo(self):
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


if __name__ == "__main__":
    unittest.main()
