import pygame
pygame.font.init()

# CONSTANTS

WIDTH = 1000
HEIGHT = 800
FPS = 60
TITLE = "Solitaire"

SGS_15 = pygame.font.SysFont("segoeuisymbol", 15)
SGS_25 = pygame.font.SysFont("segoeuisymbol", 25)
SGS_30 = pygame.font.SysFont("segoeuisymbol", 30)
SGS_40 = pygame.font.SysFont("segoeuisymbol", 40)

COLOURS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (105, 14, 14),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "BOARD": (15, 125, 60),
    "CARD BACK": (87, 56, 122),
}

CARD_VALS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["D", "H", "S", "C"]
CARD_SUIT_DISPLAY = {
    "D": u"\u2666",
    "H": u"\u2665",
    "S": u'\u2660',
    "C": u"\u2663",
}
CARD_HEIGHT = 100
CARD_WIDTH = 80
CARD_BG_OFFSET = 10

STACK_HEIGHT_OFFSET = 40
STACK_MARGIN = 20