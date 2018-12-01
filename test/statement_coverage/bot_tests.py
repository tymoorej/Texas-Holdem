import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import winning_hand
from card import Player
from card import Table

class BotTestCase(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
    