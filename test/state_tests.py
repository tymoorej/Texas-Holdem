import unittest
import pygame
import time
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from game import Game
from main import main


class ExitTestException(Exception):
    pass


class PreClickedGame(Game):
    def __init__(self, click_list):
        super().__init__()
        self.click_list = click_list
        self.click_gen = self.make_click_gen()

    def make_click_gen(self):
        for c in self.click_list:
            time.sleep(0.5)
            yield c
        raise ExitTestException()

    def get_events(self):
        print(self.state)
        click_pos = next(self.click_gen)
        pygame.mouse.set_pos(*click_pos)
        return pygame.event.get() + [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': click_pos, 'button': 1})]


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

        self.start_click = (710, 170)
        self.left_click = (60, 520)
        self.middle_click = (215, 520)
        self.right_click = (345, 520)
        self.done_click = (204, 630)

    def click_hook(self, game):
        pass

    def test_click(self):
        game = PreClickedGame([
            self.start_click,
            self.middle_click,
            self.middle_click,
            self.right_click,
        ])

        try:
            main(game)
        except ExitTestException:
            return

        self.fail("Should have exited")


if __name__ == "__main__":
    unittest.main()
