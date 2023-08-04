import settings
from card import Card
import pygame
import random

class Deck():

    def __init__(self):

        self.size = 52
        
        self.image = pygame.surface.Surface((settings.CARD_WIDTH, settings.CARD_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (settings.WIDTH - settings.CARD_WIDTH - settings.STACK_MARGIN, settings.STACK_MARGIN)
        self.image.fill(settings.COLOURS["CARD BACK"])

        self.bg_image = pygame.surface.Surface([settings.CARD_WIDTH + settings.CARD_BG_OFFSET, settings.CARD_HEIGHT + settings.CARD_BG_OFFSET])
        self.bg_rect = self.bg_image.get_rect()
        self.bg_image.fill(settings.COLOURS["BLACK"])
        self.bg_rect.topleft = (self.rect.x - (settings.CARD_BG_OFFSET // 2), self.rect.y - (settings.CARD_BG_OFFSET // 2))

        self.revealed_rect = pygame.rect.Rect(settings.WIDTH - settings.CARD_WIDTH - settings.STACK_MARGIN, settings.CARD_HEIGHT + (settings.STACK_MARGIN * 2), settings.CARD_WIDTH, settings.CARD_HEIGHT)

        self.deck = []
        self.shown = []
        self.create_deck()
        self.shuffle_deck()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def create_deck(self):
        for s in settings.CARD_SUITS:
            for v in settings.CARD_VALS:
                self.deck.append(Card(v, s, None, None))
    
    def choose(self, count):
        selected_bottom = None
        prev = None
        for i in range(count):
            selection = random.choice(self.deck)
            self.deck.remove(selection)
            self.size -= 1
            if i == 0:
                selected_bottom = selection
            if prev != None:
                prev.next = selection
                selection.prev = prev
            prev = selection

        return selected_bottom, prev
    
    def display(self, window):
        window.blit(self.bg_image, self.bg_rect.topleft)
        window.blit(self.image, self.rect.topleft)
        if len(self.shown) > 0:
            self.shown[-1].display(window)

    def turn_over(self):
        if len(self.deck) == 0:
            for d in self.shown:
                d.flip_card()
                self.deck.append(d)
            self.shown = []
        else:
            c = self.deck.pop(0)
            self.shown.append(c)
            c.flip_card()
            
            c.set_coords(*self.revealed_rect.topleft)

    def get_shown_card(self):
        return self.shown.pop()
    
    def return_to_pile(self, returned_card):
        self.shown.append(returned_card)
        returned_card.set_coords(*self.revealed_rect.topleft)
