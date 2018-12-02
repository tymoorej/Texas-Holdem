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
    def __init__(self, game, play_list, state_list, assert_equal, cards=None):
        super().__init__(cards)
        play_list = [p for p in play_list if p is not None]
        state_list = [s for s in state_list if s is not None]

        self.play_gen = self.make_play_gen(play_list)
        self.state_gen = self.make_state_gen(state_list)

        self.game = game
        self.assert_equal = assert_equal

    @staticmethod
    def make_play_gen(playlist):
        for p in playlist:
            yield p
        raise ExitTestException()

    @staticmethod
    def make_state_gen(state_list):
        for s in state_list:
            yield s
        raise ExitTestException()

    def assert_state(self, game):
        expected_state = next(self.state_gen)
        if expected_state is not None:
            self.assert_equal(expected_state, game.state)

    def bet(self, current_call, table, can_raise=True):
        self.assert_state(self.game)
        play = next(self.play_gen)

        if play == BotAction.FOLD:
            return 'Fold'

        if play == BotAction.CALL:
            chip = min(current_call, self.get_chips())
            self.remove_chips(chip)
            table.add_chips(current_call + chip)
            return -1

        if play == BotAction.ALLIN:
            chip = self.get_chips()
            self.remove_chips(chip)
            table.add_chips(chip)
            return chip

        self.remove_chips(play + current_call)
        table.add_chips(play + current_call)

        return play


class PreDeterminedGame(Game):
    def __init__(self, event_list, assert_equal):
        """
        :param event_list: A list of tuples (expected_player_state, player_event, expected_bot_state, bot_event) to be played
        """
        super().__init__()
        state_asserts, bot_asserts, player_events, bot_events  = zip(*event_list)
        self.state_gen = self.make_state_gen(state_asserts)
        self.event_gen = self.make_event_gen(player_events)
        self.bot = MockBot(self, bot_events, bot_asserts, assert_equal)
        self.assert_equal = assert_equal

    @staticmethod
    def make_event_gen(event_list):
        for e in event_list:
            # time.sleep(1)
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
        next_events = next(self.event_gen)
        self.assert_state()

        if next_events[0] == PlayerAction.ALLIN:
            # MAJOR HACK: Only works if the bot bets a maximum of once before we go all in
            # This only works because of the specific way we traverse the state graph in
            # our allin testing and that we don't go allin in other situations
            next_events = bet(self.player.get_chips() - self.table.get_chips())

        for e in next_events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.mouse.set_pos(*e.dict['pos'])

        return pygame.event.get() + next_events

    def end_game(self):
        raise ExitTestException()


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def test_player_bet_bot_call(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_FORCE, bet(5), bot_call()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_FORCE, bet(5), bot_call()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_FORCE, bet(5), bot_call()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_FORCE, bet(5), bot_call())
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.END_ROUND)
            return

        self.fail("Game should not have ended")

    def test_bot_bet_player_call(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_PREFLOP_FORCE, None, call(), None),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_FLOP_FORCE, None, call(), None),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_TURN_FORCE, None, call(), None),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_RIVER_FORCE, None, call(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.END_ROUND)
            return

        self.fail("Game should not have ended")

    def test_bet_raise_raise_call(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_FORCE, bet(100), bot_bet(100)),
            (GameState.PLAYER_PREFLOP_FORCE, GameState.BOT_PREFLOP_FORCE, bet(100), bot_call()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_FORCE, bet(100), bot_bet(100)),
            (GameState.PLAYER_FLOP_FORCE, GameState.BOT_FLOP_FORCE, bet(100), bot_call()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_FORCE, bet(100), bot_bet(100)),
            (GameState.PLAYER_TURN_FORCE, GameState.BOT_TURN_FORCE, bet(100), bot_call()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_FORCE, bet(100), bot_bet(100)),
            (GameState.PLAYER_RIVER_FORCE, GameState.BOT_RIVER_FORCE, bet(100), bot_call())
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.END_ROUND)
            return

        self.fail("Game should not have ended")

    def test_checks(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_check())

        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.END_ROUND)
            return

        self.fail("Game should not have ended")

    def test_folds(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),

            # PLAYER_PREFLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_PREFLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_PREFLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_PREFLOP_FORCE, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_PREFLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_FORCE, bet(100), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_FLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_FLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_FLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_FLOP_FORCE, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_FLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_FORCE, bet(100), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_TURN_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_TURN_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_TURN_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_TURN_FORCE, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_TURN_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_FORCE, bet(100), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_RIVER_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_RIVER_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_RIVER_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_RIVER_FORCE, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # BOT_RIVER_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_FORCE, bet(100), bot_fold()),
            (GameState.END_ROUND, None, done(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.PLAYER_PREFLOP_OPEN)
            return

        self.fail("Game should not have ended")

    def test_allins(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),

            # PLAYER_PREFLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_PREFLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_PREFLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_PREFLOP_FORCE, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_PREFLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_FORCE, bet(100), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_FLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_FLOP_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_FLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_FLOP_FORCE, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_FLOP_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_FORCE, bet(100), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_TURN_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_TURN_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_TURN_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_TURN_FORCE, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_TURN_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_FORCE, bet(100), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_RIVER_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_RIVER_OPEN
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None),

            # PLAYER_RIVER_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_OPEN, check(), bot_bet(100)),
            (GameState.PLAYER_RIVER_FORCE, GameState.ALL_IN, allin(), bot_fold()),
            (GameState.END_ROUND, None, done(), None),

            # BOT_RIVER_FORCE
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_FLOP_OPEN, GameState.BOT_FLOP_OPEN, check(), bot_check()),
            (GameState.PLAYER_TURN_OPEN, GameState.BOT_TURN_OPEN, check(), bot_check()),
            (GameState.PLAYER_RIVER_OPEN, GameState.BOT_RIVER_FORCE, bet(100), bot_allin()),
            (GameState.ALL_IN, None, fold(), None),
            (GameState.END_ROUND, None, done(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.PLAYER_PREFLOP_OPEN)
            return

        self.fail("Game should not have ended")

    def test_win_player_all_in(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.ALL_IN, allin(), bot_call()),
            (GameState.END_ROUND, None, done(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.WIN)
            return

        self.fail("Game should not have ended")

    def test_win_bot_all_in(self):
        game = PreDeterminedGame([
            (GameState.START, None, start(), None),
            (GameState.PLAYER_PREFLOP_OPEN, GameState.BOT_PREFLOP_OPEN, check(), bot_allin()),
            (GameState.ALL_IN, None, call(), None),
            (GameState.END_ROUND, None, done(), None)
        ], self.assertEqual)

        try:
            main(game)
        except ExitTestException:
            self.assertEqual(game.state, GameState.WIN)
            return

        self.fail("Game should not have ended")

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
