import settings
import pygame

class Card():

    def __init__(self, value, suit, next, prev):
        self.value = value
        self.suit = suit
        self.next = next
        self.prev = prev
        self.x = 0
        self.y = 0

        self.image = pygame.surface.Surface([settings.CARD_WIDTH, settings.CARD_HEIGHT])
        self.rect = self.image.get_rect()
        self.image.fill(settings.COLOURS["CARD BACK"])
        self.rect.topleft = (self.x, self.y)

        self.bg_image = pygame.surface.Surface([settings.CARD_WIDTH + settings.CARD_BG_OFFSET, settings.CARD_HEIGHT + settings.CARD_BG_OFFSET])
        self.bg_rect = self.bg_image.get_rect()
        self.bg_image.fill(settings.COLOURS["BLACK"])
        self.bg_rect.topleft = (self.x - (settings.CARD_BG_OFFSET // 2), self.y - (settings.CARD_BG_OFFSET // 2))

        if self.suit in ["S", "C"]:
            self.text_colour = settings.COLOURS["BLACK"]
        else:
            self.text_colour = settings.COLOURS["RED"]

        self.text = f"{self.value} {settings.CARD_SUIT_DISPLAY[self.suit]}"

        self.flipped = False


    def flip_card(self):
        self.flipped = True
        self.image.fill(settings.COLOURS["WHITE"])
    
    def set_coords(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)
        self.bg_rect.topleft = (self.x - (settings.CARD_BG_OFFSET // 2), self.y - (settings.CARD_BG_OFFSET // 2))

    def display(self, window):
        window.blit(self.bg_image, self.bg_rect.topleft)
        window.blit(self.image, self.rect.topleft)
        
        if self.flipped:
           rendered_text_small = settings.SGS_25.render(self.text, True, self.text_colour)
           window.blit(rendered_text_small, (self.x, self.y))
           window.blit(rendered_text_small, (self.x + settings.CARD_WIDTH - rendered_text_small.get_width(), self.y + settings.CARD_HEIGHT - rendered_text_small.get_height()))

    def update_linked_pos(self):
        if self.prev != None:
            self.set_coords(self.prev.x, self.prev.y + settings.STACK_HEIGHT_OFFSET)
        if self.next != None:
            self.next.update_linked_pos()