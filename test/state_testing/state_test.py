import unittest
import pygame
import time
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from game import Game, GameState
from main import main
from test.state_testing.actions import *


class ExitTestException(Exception):
    pass


class PreDeterminedGame(Game):
    def __init__(self, event_list):
        super().__init__()
        self.event_gen = self.make_event_gen(event_list)
        print(event_list)

    @staticmethod
    def make_event_gen(event_list):
        for e in event_list:
            time.sleep(1)
            yield e
        raise ExitTestException()

    def get_events(self):
        print(self.state)
        next_events = next(self.event_gen)

        for e in next_events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_pos(*e.dict['pos'])

        return pygame.event.get() + next_events


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_start(self):
        game = PreDeterminedGame([
            start()
        ])

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.PLAYER_PREFLOP_OPEN)
            return

        self.fail("Game should not have ended")

    def test_check(self):
        game = PreDeterminedGame([
            start(),
            check(),
            bet(300)
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
