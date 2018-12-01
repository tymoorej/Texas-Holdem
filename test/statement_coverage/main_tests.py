import unittest
import asyncio
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../..'))


from card import *
from winning_hand import *
from bot import Monte_Carlo, MONTE_CARLO_ITERATIONS
from random import randint, shuffle
from main import *
from game import Game
import time
from mock import *
import pygame

os.chdir("..")
os.chdir("..")

class emptyClass():

    def __init__(self):
        pass

class mainGame(Game):

    def __init__(self):
        super().__init__()
        window = Mock(spec = ['blit()'])
        clock = Mock(spec = ['tick()'])
        self.clock = clock()
        self.window = window()
        self.color = None

    def get_events(self):
        #obj = someobject
        obj = emptyClass()
        setattr(obj, 'type', pygame.MOUSEBUTTONDOWN)
        setattr(obj, 'dict', {'pos': (695, 155)})
        return [obj]




class ExampleTestCase(unittest.TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self._number_of_tests = 1000
        self.color = None

    def mouseTest():
        return

    def drawRect(window, color, rect):
        return

    @patch('pygame.display')
    @patch('pygame.font')
    @patch('pygame.mouse.get_pos', side_effect=mouseTest)
    @patch('pygame.draw.rect', side_effect=drawRect)
    def test_start_screen(self, display, font, getPosition, draw):
    
        #Test Set One
        getPosition.return_value = (695, 155)
        game = mainGame()
        start_screen(game)

        start_screen(game)







if __name__ == "__main__":
    unittest.main()
