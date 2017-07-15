'''
This file sets up all the global vairables needed for the pygame visualization
'''
import pygame

pygame.init() # setup pygame

width = 1300
height = 700
black = (0, 0, 0)
white=(255,255,255)
grey=(200,200,200)

Window = pygame.display.set_mode((width, height))  # initializes the window
pygame.display.set_caption("Texas Holdem") # Title of window

clock = pygame.time.Clock() # used for fps

Title_image=pygame.image.load("PNG-cards-1.3/title_image.png") # title image
Title_image = pygame.transform.scale(Title_image,(width,height)) # resizing

empty_table=pygame.image.load("PNG-cards-1.3/empty_table.jpg") # empty table
empty_table = pygame.transform.scale(empty_table,(width,height)) # resizing

game_over=False # true when game is over
