import pygame


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


def check():
    return click((215, 520))


def call():
    return click((215, 520))


def fold():
    return click((345, 520))


def done():
    return click((204, 630))

