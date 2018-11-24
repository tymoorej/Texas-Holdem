"""
This file sets up all the global variables needed for the pygame visualization
"""
import pygame
import enum

PRE_FLOP = 0
FLOP = 1
TURN = 2
RIVER = 3


class GameException(Exception):
    pass


class GameState(enum.Enum):
    START = -1
    PLAYER_PREFLOP_OPEN = 0
    PLAYER_PREFLOP_FORCE = 1
    BOT_PREFLOP_OPEN = 2
    BOT_PREFLOP_FORCE = 3
    PLAYER_FLOP_OPEN = 4
    PLAYER_FLOP_FORCE = 5
    BOT_FLOP_OPEN = 6
    BOT_FLOP_FORCE = 7
    PLAYER_TURN_OPEN = 8
    PLAYER_TURN_FORCE = 9
    BOT_TURN_OPEN = 10
    BOT_TURN_FORCE = 11
    PLAYER_RIVER_OPEN = 12
    PLAYER_RIVER_FORCE = 13
    BOT_RIVER_OPEN = 14
    BOT_RIVER_FORCE = 15
    ALL_IN = 17
    END_ROUND = 18

    @staticmethod
    def calc_state(table, player_turn, force):
        table_card_count = len(table.get_cards())
        if table_card_count == 0:
            turn = PRE_FLOP
        elif table_card_count == 3:
            turn = FLOP
        elif table_card_count == 4:
            turn = TURN
        elif table_card_count == 5:
            turn = RIVER
        else:
            raise GameException("Invalid amount of cards on the table")

        return GameState(turn * 4 + (not player_turn) * 2 + force)


class Game:
    def __init__(self):
        self.state = None
        self.state_history = []
        self.width = 1300
        self.height = 700
        self.window = None
        self.clock = None  # used for fps
        self.game_over = False  # true when game is over
        self.title_image = None  # title image
        self.empty_table = None  # empty table image

    def init(self):
        pygame.init()  # setup pygame

        self.window = pygame.display.set_mode((self.width, self.height))  # initializes the window
        pygame.display.set_caption("Texas Holdem")  # Title of window

        self.clock = pygame.time.Clock()

        self.title_image = pygame.image.load("PNG-cards-1.3/title_image.png")
        self.title_image = pygame.transform.scale(self.title_image, (self.width, self.height))  # resizing

        self.empty_table = pygame.image.load("PNG-cards-1.3/empty_table.jpg")
        self.empty_table = pygame.transform.scale(self.empty_table, (self.width, self.height))  # resizing

        self.game_over = False

    def set_game_state(self, state):
        self.state = state
        self.state_history.append(state)

    def infer_state(self, player_turn, table, current_call, can_raise, done):
        if done:
            self.set_game_state(GameState.END_ROUND)
            return

        if not can_raise:
            self.set_game_state(GameState.ALL_IN)
            return

        self.set_game_state(GameState.calc_state(table, player_turn, current_call > 0))
        return

    def get_events(self):
        return pygame.event.get()

    def is_over(self):
        return self.game_over
