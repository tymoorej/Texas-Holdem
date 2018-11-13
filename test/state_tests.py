import unittest
import pygame

from main import setup, rounds, end_of_round, player_bet, game_over


class DoneFlag:
    def __init__(self):
        self._done = False

    def set(self, val):
        self._done = val

    def done(self):
        return self._done


def mainloop(hook):
    done_flag = DoneFlag()
    cards, table, player, bot = setup()
    while not done_flag.done():
        skip = rounds(cards, table, player, bot)
        end_of_round(cards, table, player, bot, skip)
        player_bet(0, player, bot, table, done=True)
        hook(done_flag)
        if game_over or player.get_chips() <= 0 or bot.get_chips() <= 0:
            pygame.quit()
            quit()
        cards.collect([player, bot, table])


class StateTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)

    def done_hook(self, done_flag):
        done_flag.set(True)

    def test_example(self):
        mainloop(self.done_hook)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
