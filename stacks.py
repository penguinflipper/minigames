import settings
import pygame

class Stack():

    def __init__(self, size, x, y, initial_card, tail):
        self.head = initial_card #index 0 => bottom card, index -1 => top card (flipped)
        self.tail = tail
        self.size = size

        self.x = x
        self.y = y

        if self.tail != None:
            self.tail.flip_card()
        self.offset_cards()
        if self.tail != None:
            self.bottom_y = self.tail.y + settings.CARD_HEIGHT
        else:
            self.bottom_y = self.y + settings.CARD_HEIGHT

        self.image = pygame.surface.Surface([settings.CARD_WIDTH + settings.CARD_BG_OFFSET, settings.CARD_HEIGHT + settings.CARD_BG_OFFSET])
        self.rect = self.image.get_rect()
        self.image.fill(settings.COLOURS["BLACK"])
        self.rect.topleft = (self.x - (settings.CARD_BG_OFFSET // 2), self.y - (settings.CARD_BG_OFFSET // 2))

    def offset_cards(self):
        y = self.y

        c = self.head
        while c != None:
            c.set_coords(self.x, y)
            y += settings.STACK_HEIGHT_OFFSET
            c = c.next

    def display(self, window):
        window.blit(self.image, self.rect.topleft)
        c = self.head
        while c != None:
            c.display(window)
            c = c.next

    def select_substack(self, mpy):
        substack = None
        c = self.head
        
        while c != None:
            if c.flipped:
                if mpy > c.y:
                    if c.next != None:
                        if mpy < c.y + settings.STACK_HEIGHT_OFFSET:
                            substack = c
                    else:
                        if mpy < c.y + settings.CARD_HEIGHT:
                            substack = c
                    if substack != None:
                        if c.prev != None:
                            self.tail = c.prev
                            c.prev.next = None
                            c.prev = None
                            self.bottom_y = self.tail.y + settings.CARD_HEIGHT
                        if c == self.head:
                            self.head = None
                            self.tail = None
                        break
            c = c.next
        
        if c != None:
            if c.flipped:
                return substack
        return None
    
    def update_tail(self):
        c = self.head
        
        while c != None:
            self.tail = c
            self.bottom_y = self.tail.y + settings.CARD_HEIGHT
            c = c.next

    def compare_stacks(self, other):
        try:
            if settings.CARD_VALS[settings.CARD_VALS.index(other.value) + 1] == self.tail.value:
                return (self.tail.suit in ["D", "H"] and other.suit in ["S", "C"]) or (self.tail.suit in ["S", "C"] and other.suit in ["D", "H"])
            return False
        except:
            return False
    
    def flip_last(self):
        if self.tail != None:
            self.tail.flip_card()

    def compare_final_stack(self, other):
        try:
            if settings.CARD_VALS[settings.CARD_VALS.index(other.value) - 1] == self.tail.value:
                return self.tail.suit == other.suit
            return False
        except:
            return False