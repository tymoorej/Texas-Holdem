import unittest
import pygame
import time
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from game import Game, GameState
from main import main


class ExitTestException(Exception):
    pass


class PreClickedGame(Game):
    def __init__(self, click_list):
        super().__init__()
        self.click_gen = self.make_click_gen(click_list)

    @staticmethod
    def make_click_gen(click_list):
        for c in click_list:
            time.sleep(1)
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

    def test_start(self):
        game = PreClickedGame([
            self.start_click,
        ])

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.PLAYER_PREFLOP_OPEN)
            return

        self.fail("Game should not have ended")

    def test_check(self):
        game = PreClickedGame([
            self.start_click,
            self.middle_click,
        ])

        try:
            main(game)
        except ExitTestException:
            self.assertTrue(
                game.state == GameState.PLAYER_PREFLOP_FORCE or
                game.state == GameState.PLAYER_FLOP_OPEN
            )
            return

        self.fail("Game should not have ended")

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
