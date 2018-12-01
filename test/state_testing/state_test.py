import unittest
import time
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from game import Game, GameState
from main import main
from card import Bot
from test.state_testing.actions import *


class ExitTestException(Exception):
    pass


class MockBot(Bot):
    def __init__(self, playlist, cards=None):
        super().__init__(cards)
        self.play_gen = self.make_play_gen(playlist)

    @staticmethod
    def make_play_gen(playlist):
        for p in playlist:
            yield p
        raise ExitTestException()

    def bet(self, current_call, table, can_raise=True):
        play = next(self.play_gen)

        if play == BotAction.CALL:
            chip = min(current_call, self.get_chips())
            self.remove_chips(chip)
            table.add_chips(chip)
            return -1

        if play is int:
            self.remove_chips(play + current_call)
            table.add_chips(play + current_call)

        return play


class PreDeterminedGame(Game):
    def __init__(self, event_list, assert_equal):
        """
        :param event_list: A list of tuples (player_event, bot_event) to be played
        """
        super().__init__()
        state_asserts, player_events, bot_events,  = zip(*event_list)
        bot_events = [e for e in bot_events if e is not None]
        self.state_gen = self.make_state_gen(state_asserts)
        self.event_gen = self.make_event_gen(player_events)
        self.bot = MockBot(bot_events)
        self.assert_equal = assert_equal

    @staticmethod
    def make_event_gen(event_list):
        for e in event_list:
            time.sleep(1)
            yield e
        raise ExitTestException()

    @staticmethod
    def make_state_gen(state_list):
        for s in state_list:
            yield s
        raise ExitTestException()

    def assert_state(self):
        expected_state = next(self.state_gen)
        if expected_state is not None:
            self.assert_equal(expected_state, self.state)

    def get_events(self):
        self.assert_state()
        next_events = next(self.event_gen)

        for e in next_events:
            print(e)
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_pos(*e.dict['pos'])

        return pygame.event.get() + next_events


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_start(self):
        game = PreDeterminedGame([
            (GameState.START, start(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.PLAYER_PREFLOP_OPEN)
            return

        self.fail("Game should not have ended")

    def test_check(self):
        game = PreDeterminedGame([
            (GameState.START, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, check(), bot_check())
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(GameState.PLAYER_FLOP_OPEN, game.state)
            return

        self.fail("Game should not have ended")

    def test_bet(self):
        game = PreDeterminedGame([
            (GameState.START, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, bet(300), bot_call())
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEquals(GameState.PLAYER_TURN_OPEN, game.state)
            return

        self.fail("Game should not have ended")

    def test_round(self):
        game = PreDeterminedGame([
            (GameState.START, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, check(), bot_check()),   # PREFLOP
            (GameState.PLAYER_FLOP_OPEN, bet(300), bot_call()),      # FLOP
            (GameState.PLAYER_TURN_OPEN, check(), bot_bet(500)),     # TURN
            (GameState.PLAYER_TURN_FORCE, call(), None),
            (GameState.PLAYER_RIVER_OPEN, check(), bot_check()),     # RIVER
            (GameState.END_ROUND, done(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEquals(GameState.PLAYER_PREFLOP_OPEN, game.state)
            return

        self.fail("Game should not have ended")

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
