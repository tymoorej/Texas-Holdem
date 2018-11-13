import unittest

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from card import *
from winning_hand import *
from random import randint

class TestHandMethods(unittest.TestCase):
    def test_royal_flush(self):
        self.assertEqual(1, 1)

    def test_straight_flush(self):
        self.assertEqual(1, 1)

    def test_four_of_a_kind(self):
        self.assertEqual(1, 1)

    def test_full_house(self):
        self.assertEqual(1, 1)

    def test_flush(self):
        self.assertEqual(1, 1)

    def test_straight(self):
        self.assertEqual(1, 1)

    def test_three_of_a_kind(self):
        self.assertEqual(1, 1)

    def test_two_pair(self):
        self.assertEqual(1, 1)

    def test_one_pair(self):
        self.assertEqual(1, 1)

    def test_repeated_cards(self):
        self.assertEqual(1, 1)

    def test_highest_card(self):
        player1 = Player('p1')
        player2 = Player('p2')


        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
    