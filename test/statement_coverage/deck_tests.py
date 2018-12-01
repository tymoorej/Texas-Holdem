import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../..'))


class DeckTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_initializer(self):
        pass

    def test_print_cards(self):
        pass

    def test_get_cards(self):
        pass

    def test_shuffle(self):
        pass

    def test_remove_random_card(self):
        pass

    def test_remove_top_card(self):
        pass

    def test_remove_card(self):
        pass

    def test_deal(self):
        pass

    def test_collect(self):
        pass

    def test_have_all_cards(self):
        pass

    def test_push_to_table(self):
        pass


if __name__ == '__main__':
    unittest.main()
