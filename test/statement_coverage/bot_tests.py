import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from card import Table
from card import Bot
from bot import bot_bet

class BotTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self._suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']

        # royal flush, bot has 100% chance to win, therefore we can always modify the calculated
        # chance by changing the rand_number_in_range method
        self._bot = Bot()
        self._table = Table()
        card_suit = self._suits[0]
        cards = []
        for i in range(10,15): 
                cards.append((i,card_suit))
        for i,s in enumerate(cards):
                if i <= 1:
                    self._bot.add_card(s)
                else:
                    self._table.add_card(s)

    def execute(self, chance, current_call, chips, can_raise = True):
        self._bot.remove_chips(self._bot.get_chips())
        self._bot.add_chips(chips)

        old_method = Bot.rand_number_in_range

        def new_method(self, a, b):
            return chance - 100
        
        Bot.rand_number_in_range = new_method

        result = bot_bet(current_call, self._bot, self._table, can_raise)

        Bot.rand_number_in_range = old_method

        return result

    def test_bot_bet1(self):
        result = self.execute(-15, 10, 5)
        self.assertEqual(result, 'Fold')

    def test_bot_bet2(self):
        result = self.execute(115, 10, 15)        
        self.assertEqual(result, 15-10)

    def test_bot_bet3(self):
        result = self.execute(115, 10, 5)        
        self.assertEqual(result, -1)
    
    def test_bot_bet4(self):
        result = self.execute(40, 10, 5)        
        self.assertEqual(result, -1)

    def test_bot_bet5(self):
        result = self.execute(40, 5, 10)        
        self.assertEqual(result, -1)

    def test_bot_bet6(self):
        result = self.execute(100, None, 10)        
        self.assertEqual(result, 10)

    def test_bot_bet7(self):
        result = self.execute(35, None, 10)        
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
    