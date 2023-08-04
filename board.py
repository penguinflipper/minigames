import settings
from stacks import Stack
from deck import Deck
import pygame

class Board():

    def __init__(self, instance):

        self.width = settings.WIDTH
        self.height = settings.HEIGHT
        self.image = pygame.surface.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.image.fill(settings.COLOURS["BOARD"])

        self.instance = instance
        self.deck = Deck()
        self.stacks = {}
        self.create_starting_stacks()

        self.changing_stack = None

        self.final_suit_stacks = {}
        self.changing_final_stack = None
        self.init_final_stacks()

    def create_starting_stacks(self):
        x = settings.STACK_MARGIN
        y = settings.STACK_MARGIN

        for i in range(1, 8):
            stack_cards, tail = self.deck.choose(i)
            self.stacks[i] = Stack(i, x, y, stack_cards, tail)
            x += settings.STACK_MARGIN + settings.CARD_WIDTH

    def init_final_stacks(self):
        y = settings.HEIGHT - settings.STACK_MARGIN - settings.CARD_HEIGHT

        for i in range(1, 5):
            x = settings.WIDTH - (settings.CARD_WIDTH*(i)) - (settings.STACK_MARGIN*i)
            self.final_suit_stacks[i] = Stack(i, x, y, None, None)
            

    def display(self):
        self.instance.window.blit(self.image, self.rect.topleft)

        for s in self.stacks.values():
            s.display(self.instance.window)

        for t in self.final_suit_stacks.values():
            t.display(self.instance.window)

        self.deck.display(self.instance.window)

    def select_stack(self, mouse_pos):
        mpx, mpy = mouse_pos

        clicked_stack = None

        for cs in self.stacks.values():
            if mpx > cs.x and mpx < cs.x + settings.CARD_WIDTH:
                if mpy > cs.y and mpy < cs.bottom_y:
                    clicked_stack = cs
                    break
        
        if clicked_stack != None:
            substack_first_card = clicked_stack.select_substack(mpy)
            if substack_first_card != None:
                self.changing_stack = clicked_stack
                return True, substack_first_card
        return False, None
    
    def add_to_stack(self, mouse_pos, stk):
        mpx, mpy = mouse_pos
        for cs in self.stacks.values():
            if mpx > cs.x and mpx < cs.x + settings.CARD_WIDTH:
                if cs.tail != None:
                    if mpy > cs.tail.y and mpy < cs.tail.y + settings.CARD_HEIGHT:
                        if cs.compare_stacks(stk):
                            cs.tail.next = stk
                            stk.prev = cs.tail
                            stk.update_linked_pos()
                            cs.update_tail()
                            self.flip_last_of_stack()
                            self.changing_stack = None
                            return True
                        break
                else:
                    if mpy > cs.y and mpy < cs.bottom_y:
                        if stk.value == "K":
                            cs.head = stk
                            stk.set_coords(cs.x, cs.y)
                            stk.update_linked_pos()
                            cs.update_tail()
                            self.flip_last_of_stack()
                            self.changing_stack = None
                            return True
                    break
        return False
    
    def flip_last_of_stack(self):
        self.changing_stack.flip_last()

    def reset_held_stack(self, stk):
        if self.changing_stack.head == None:
            self.changing_stack.head = stk
            stk.set_coords(self.changing_stack.x, self.changing_stack.y)
        else:
            self.changing_stack.tail.next = stk
            stk.prev = self.changing_stack.tail
        
        self.changing_stack.update_tail()
        stk.update_linked_pos()
        self.changing_stack = None

    def check_show_deck_click(self, x, y):
        return self.deck.rect.collidepoint(x, y)
    
    def take_deck_card_click(self, x, y):
        return self.deck.revealed_rect.collidepoint(x, y)
            
    def show_next(self):
        self.deck.turn_over()

    def take_deck_card(self):
        return True, self.deck.get_shown_card()
    
    def add_deck_to_stack(self, mouse_pos, stk):
        mpx, mpy = mouse_pos
        for cs in self.stacks.values():
            if mpx > cs.x and mpx < cs.x + settings.CARD_WIDTH:
                if cs.tail != None:
                    if mpy > cs.tail.y and mpy < cs.tail.y + settings.CARD_HEIGHT:
                        if cs.compare_stacks(stk):
                            cs.tail.next = stk
                            stk.prev = cs.tail
                            stk.update_linked_pos()
                            cs.update_tail()
                            if self.changing_final_stack != None:
                                self.changing_final_stack = None
                            return True
                        break
                else:
                    if mpy > cs.y and mpy < cs.bottom_y:
                        if stk.value == "K":
                            cs.head = stk
                            stk.set_coords(cs.x, cs.y)
                            stk.update_linked_pos()
                            cs.update_tail()
                            if self.changing_final_stack != None:
                                self.changing_final_stack = None
                            return True
                    break
        return False
    
    def return_to_deck(self, deck_card):
        self.deck.return_to_pile(deck_card)
    
    def add_to_suit_stack(self, mp, card):
        for s in self.final_suit_stacks.values():
            if s.rect.collidepoint(mp):
                if s.head == None:
                    if card.value == "A":
                        s.head = card
                        card.set_coords(s.x, s.y)
                        card.next = None
                        s.update_tail()
                        return True
                else:
                    if s.compare_final_stack(card):
                        s.tail.next = card
                        card.prev = s.tail
                        card.set_coords(s.x, s.y)
                        card.next = None
                        s.update_tail()
                        return True
        return False
    
    def check_final_stk_click(self, mp):
        for s in self.final_suit_stacks.values():
            if s.rect.collidepoint(mp):
                return True
        return False
    
    def take_from_final_stack(self, mp):
        for s in self.final_suit_stacks.values():
            if s.rect.collidepoint(mp) and s.tail != None:
                c = s.tail
                self.changing_final_stack = s
                if s.head == c:
                    s.head = None
                    s.tail = None
                else:
                    c.prev.next = None
                    c.prev = None
                    s.update_tail()
                return True, c
        return False, None
    
    def return_to_final_stk(self, stk_card):
        if self.changing_final_stack.head == None:
            self.changing_final_stack.head = stk_card
        else:
            self.changing_final_stack.tail.next = stk_card
            stk_card.prev = self.changing_final_stack.tail

        stk_card.set_coords(self.changing_final_stack.x, self.changing_final_stack.y)
        self.changing_final_stack.update_tail()
        self.changing_final_stack = None