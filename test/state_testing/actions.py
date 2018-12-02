import pygame
import enum


class PlayerAction(enum.Enum):
    ALLIN = -1


class BotAction(enum.Enum):
    CALL = 4
    FOLD = 5
    ALLIN = 6


def click(click_pos):
    return [pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': click_pos, 'button': 1})]


def start():
    return click((710, 170))


def bet(amt):
    bet_events = click((60, 520))

    for digit in str(amt):
        bet_events.append(pygame.event.Event(pygame.KEYDOWN, {'unicode': digit}))

    bet_events.append(pygame.event.Event(pygame.KEYDOWN, {'unicode': '\n', 'key': pygame.K_RETURN}))

    return bet_events


def allin():
    return [PlayerAction.ALLIN]


def check():
    return click((215, 520))


def call():
    return click((215, 520))


def fold():
    return click((345, 520))


def done():
    return click((204, 630))


def bot_bet(amt):
    return amt


def bot_check():
    return 0


def bot_call():
    return BotAction.CALL


def bot_fold():
    return BotAction.FOLD


def bot_allin():
    return BotAction.ALLIN
