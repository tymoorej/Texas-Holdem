"""
This file sets up all the global variables needed for the pygame visualization
"""
import pygame
import enum


class GameState(enum.Enum):
    START = 0


class Game:
    def __init__(self):
        self.state = GameState.START
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

    def get_events(self):
        return pygame.event.get()

    def is_over(self):
        return self.game_over
