import unittest
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

# sys.path.insert(1, os.path.join(sys.path[0], '..'))
from card import Bot


class BotTestCase(unittest.TestCase):

    def setUp(self):
        self.bot_cards = [
            (2, 'Spades'),
            (7, 'Hearts'),
        ]

    def test_constructs(self):
        bot = Bot()
        self.assertEqual(0, len(bot.get_cards()))
        self.assertGreater(bot.get_chips(), 0)

        bot = Bot(self.bot_cards)
        self.assertEqual(len(self.bot_cards), len(bot.get_cards()))


if __name__ == '__main__':
    unittest.main()
