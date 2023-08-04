import settings
from board import Board
import pygame


class Game():

    def __init__(self):
        
        pygame.display.init()
        
        self.window = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.FPS = settings.FPS

        self.running = False

    def run(self):
        self.running = True
        self.BOARD = Board(self)
        
        self.holding_stack = False
        self.holding_bottom_card = None

        self.holding_deck_card = False
        self.deck_card = None

        self.holding_final_stk_card = False
        self.final_stk_card = None

        self.game_loop()

    def game_loop(self):

        while self.running:
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.render()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:

                    if self.BOARD.check_show_deck_click(*pygame.mouse.get_pos()):
                        self.BOARD.show_next()
                    elif self.BOARD.take_deck_card_click(*pygame.mouse.get_pos()):
                        if self.holding_deck_card == False:
                            self.holding_deck_card, self.deck_card = self.BOARD.take_deck_card()
                    elif self.holding_deck_card:
                        added = self.BOARD.add_deck_to_stack(pygame.mouse.get_pos(), self.deck_card)
                        if added:
                            self.holding_deck_card = False
                            self.deck_card = None
                        else:
                            final_deck_placed = self.BOARD.add_to_suit_stack(pygame.mouse.get_pos(), self.deck_card)
                            if final_deck_placed:
                                self.holding_deck_card = False
                                self.deck_card = None

                    elif self.BOARD.check_final_stk_click(pygame.mouse.get_pos()) and self.holding_stack == False:
                        if self.holding_final_stk_card:
                            final_card_replace = self.BOARD.add_to_suit_stack(pygame.mouse.get_pos(), self.final_stk_card)
                            if final_card_replace:
                                self.holding_final_stk_card = False
                                self.final_stk_card = None
                        else:
                            self.holding_final_stk_card, self.final_stk_card = self.BOARD.take_from_final_stack(pygame.mouse.get_pos())

                    elif self.holding_final_stk_card:
                        temps = self.BOARD.add_to_stack(pygame.mouse.get_pos(), self.final_stk_card)
                        if temps:
                            self.holding_final_stk_card = False
                            self.final_stk_card = None
                    
                    else:
                        if self.holding_stack == False:
                            self.holding_stack, self.holding_bottom_card = self.BOARD.select_stack(pygame.mouse.get_pos())
                        elif self.holding_stack:
                            placed = self.BOARD.add_to_stack(pygame.mouse.get_pos(), self.holding_bottom_card)
                            if placed:
                                self.holding_stack = False
                                self.holding_bottom_card = None
                            else:
                                if self.holding_bottom_card.next == None:
                                    final_placed = self.BOARD.add_to_suit_stack(pygame.mouse.get_pos(), self.holding_bottom_card)
                                    if final_placed:
                                        self.BOARD.flip_last_of_stack()
                                        self.holding_stack = False
                                        self.holding_bottom_card = None

                elif pygame.mouse.get_pressed()[2]:
                    if self.holding_stack:
                        self.BOARD.reset_held_stack(self.holding_bottom_card)
                        self.holding_stack = False
                        self.holding_bottom_card = None
                    elif self.holding_deck_card:
                        self.BOARD.return_to_deck(self.deck_card)
                        self.holding_deck_card = False
                        self.deck_card = None
                    elif self.holding_final_stk_card:
                        self.BOARD.return_to_final_stk(self.final_stk_card)
                        self.holding_final_stk_card = False
                        self.final_stk_card = None


    def update(self):
        if self.holding_stack:
            self.holding_bottom_card.set_coords(*pygame.mouse.get_pos())
            self.holding_bottom_card.update_linked_pos()
        
        elif self.holding_deck_card:
            self.deck_card.set_coords(*pygame.mouse.get_pos())
            self.deck_card.update_linked_pos()

        elif self.holding_final_stk_card:
            self.final_stk_card.set_coords(*pygame.mouse.get_pos())
        

    def render(self):
        self.window.fill(settings.COLOURS["BLACK"])
        
        self.BOARD.display()
        
        if self.holding_stack:
            c = self.holding_bottom_card
            while c != None:
                c.display(self.window)
                c = c.next
        
        elif self.holding_deck_card:
            self.deck_card.display(self.window)

        elif self.holding_final_stk_card:
            self.final_stk_card.display(self.window)

        pygame.display.flip()

instance = Game()
instance.run()