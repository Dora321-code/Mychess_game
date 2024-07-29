import os
import pygame
from pygame.locals import *
from piece import Piece
from chess import Chess
from utils import Utils

class Game:
    def __init__(self):
        # screen dimensions
        screen_width = 640
        screen_height = 750
        # flag to know if game menu has been showed
        self.menu_showed = False
        # flag to set game loop
        self.running = True
        # base folder for program resources
        self.resources = "res"
        
        # initialize game window
        pygame.display.init()
        # initialize font for text
        pygame.font.init()

        # create game window
        self.screen = pygame.display.set_mode([screen_width, screen_height])

        # title of window
        window_title = "Chess"
        # set window caption
        pygame.display.set_caption(window_title)

        # get location of game icon
        icon_src = os.path.join(self.resources, "chess_icon.png")
        # load game icon
        icon = pygame.image.load(icon_src)
        # set game icon
        pygame.display.set_icon(icon)
        # update display
        pygame.display.flip()
        # set game clock
        self.clock = pygame.time.Clock()

        # Load background image
        self.bg_image = pygame.image.load(os.path.join(self.resources, "background.jpeg")).convert()

    def start_game(self):
        """Function containing main game loop""" 
        # chess board offset
        self.board_offset_x = 0
        self.board_offset_y = 50
        self.board_dimensions = (self.board_offset_x, self.board_offset_y)
        
        # get location of chess board image
        board_src = os.path.join(self.resources, "board.png")
        # load the chess board image
        self.board_img = pygame.image.load(board_src).convert()

        # get the width of a chess board square
        square_length = self.board_img.get_rect().width // 8

        # initialize list that stores all places to put chess pieces on the board
        self.board_locations = []

        # calculate coordinates of the each square on the board
        for x in range(0, 8):
            self.board_locations.append([])
            for y in range(0, 8):
                self.board_locations[x].append([self.board_offset_x+(x*square_length), 
                                                self.board_offset_y+(y*square_length)])

        # get location of image containing the chess pieces
        pieces_src = os.path.join(self.resources, "pieces.png")
        # create class object that handles the gameplay logic
        self.chess = Chess(self.screen, pieces_src, self.board_locations, square_length)

        # game loop
        while self.running:
            self.clock.tick(5)
            # poll events
            for event in pygame.event.get():
                # get keys pressed
                key_pressed = pygame.key.get_pressed()
                # check if the game has been closed by the user
                if event.type == pygame.QUIT or key_pressed[K_ESCAPE]:
                    # set flag to break out of the game loop
                    self.running = False
                elif key_pressed[K_SPACE]:
                    self.chess.reset()
            
            winner = self.chess.winner

            if not self.menu_showed:
                self.menu()
            elif len(winner) > 0:
                self.declare_winner(winner)
            else:
                self.game()
            
            # update display
            pygame.display.flip()
            # update events
            pygame.event.pump()

        # call method to stop pygame
        pygame.quit()
    

    def menu(self):
        """method to show game menu"""
        # draw background image
        self.screen.blit(self.bg_image, (0, 0))
        
        # black color
        black_color = (0, 0, 0)
        # coordinates for "Play" button
        start_btn = pygame.Rect(270, 300, 100, 50)
        # coordinates for "Help" button
        help_btn = pygame.Rect(270, 360, 100, 50)
        # coordinates for "Settings" button
        settings_btn = pygame.Rect(270, 420, 100, 50)
        # coordinates for "Rules" button
        rules_btn = pygame.Rect(270, 480, 100, 50)
        
        # show buttons
        pygame.draw.rect(self.screen, black_color, start_btn)
        pygame.draw.rect(self.screen, black_color, help_btn)
        pygame.draw.rect(self.screen, black_color, settings_btn)
        pygame.draw.rect(self.screen, black_color, rules_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the game menu
        welcome_text = big_font.render("My Chess", False, black_color)
        created_by = small_font.render("Created by Isdora", True, white_color)
        start_btn_label = small_font.render("Play", True, white_color)
        help_btn_label = small_font.render("Help", True, white_color)
        settings_btn_label = small_font.render("About", True, white_color)
        rules_btn_label = small_font.render("Rules", True, white_color)
        
        # show welcome text
        self.screen.blit(welcome_text, 
                      ((self.screen.get_width() - welcome_text.get_width()) // 2, 
                      150))
        # show credit text
        self.screen.blit(created_by, 
                      ((self.screen.get_width() - created_by.get_width()) // 2, 
                      self.screen.get_height() - created_by.get_height() - 100))
        # show text on the buttons
        self.screen.blit(start_btn_label, 
                      ((start_btn.x + (start_btn.width - start_btn_label.get_width()) // 2, 
                      start_btn.y + (start_btn.height - start_btn_label.get_height()) // 2)))
        self.screen.blit(help_btn_label, 
                      ((help_btn.x + (help_btn.width - help_btn_label.get_width()) // 2, 
                      help_btn.y + (help_btn.height - help_btn_label.get_height()) // 2)))
        self.screen.blit(settings_btn_label, 
                      ((settings_btn.x + (settings_btn.width - settings_btn_label.get_width()) // 2, 
                      settings_btn.y + (settings_btn.height - settings_btn_label.get_height()) // 2)))
        self.screen.blit(rules_btn_label, 
                      ((rules_btn.x + (rules_btn.width - rules_btn_label.get_width()) // 2, 
                      rules_btn.y + (rules_btn.height - rules_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if "Play" button was clicked
            if start_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, start_btn, 3)
                
                # change menu flag
                self.menu_showed = True
            # check if "Help" button was clicked
            elif help_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # call help method
                self.show_help()
            # check if "Settings" button was clicked
            elif settings_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # call settings method
                self.show_settings()
            # check if "Rules" button was clicked
            elif rules_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # call rules method
                self.show_rules()
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = True

    def show_help(self):
        """method to show help screen"""
        # draw background image
        self.screen.blit(self.bg_image, (0, 0))
        
        # black color
        black_color = (0, 0, 0)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 40)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the help screen
        help_text = big_font.render("Help", False, black_color)
        instructions = [
            "Use arrow keys to move pieces.",
            "Press SPACE to reset the game.",
            "Press ESC to quit."
        ]
        help_instructions = [small_font.render(line, True, black_color) for line in instructions]
        
        # show help text
        self.screen.blit(help_text, 
                      ((self.screen.get_width() - help_text.get_width()) // 2, 
                      100))
        # show instructions
        for i, line in enumerate(help_instructions):
            self.screen.blit(line, 
                          ((self.screen.get_width() - line.get_width()) // 2, 
                          200 + i * 30))

        # update display
        pygame.display.flip()
        # wait for user input to go back to menu
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    waiting = False

    def show_settings(self):
        """method to show settings screen"""
        # draw background image
        self.screen.blit(self.bg_image, (0, 0))
        
        # black color
        black_color = (0, 0, 0)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 40)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the about screen
        settings_text = big_font.render("About", False, black_color)
        settings_info = small_font.render("My Chess @2024", True, black_color)
        
        # show settings text
        self.screen.blit(settings_text, 
                      ((self.screen.get_width() - settings_text.get_width()) // 2, 
                      100))
        # show settings info text
        self.screen.blit(settings_info, 
                      ((self.screen.get_width() - settings_info.get_width()) // 2, 
                      200))

        # update display
        pygame.display.flip()
        # wait for user input to go back to menu
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    waiting = False

    def show_rules(self):
        """method to show rules screen"""
        # draw background image
        self.screen.blit(self.bg_image, (0, 0))
        
        # black color
        black_color = (0, 0, 0)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 40)
        small_font = pygame.font.SysFont("comicsansms", 20)
        # create text to be shown on the rules screen
        rules_text = big_font.render("Rules", False, black_color)
        rules = [
            "1. White moves first.",
            "2. Each player takes turns to move one piece.",
            "3. The goal is to checkmate the opponent's king."
        ]
        rules_info = [small_font.render(line, True, black_color) for line in rules]
        
        # show rules text
        self.screen.blit(rules_text, 
                      ((self.screen.get_width() - rules_text.get_width()) // 2, 
                      100))
        # show rules info text
        for i, line in enumerate(rules_info):
            self.screen.blit(line, 
                          ((self.screen.get_width() - line.get_width()) // 2, 
                          200 + i * 30))

        # update display
        pygame.display.flip()
        # wait for user input to go back to menu
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    waiting = False

    def game(self):
        # background color
        color = (0,0,0)
        # set backgound color
        self.screen.fill(color)
        
        # show the chess board
        self.screen.blit(self.board_img, self.board_dimensions)

        # call self.chess. something
        self.chess.play_turn()
        # draw pieces on the chess board
        self.chess.draw_pieces()


    def declare_winner(self, winner):
        # background color
        bg_color = (255, 255, 255)
        # set background color
        self.screen.fill(bg_color)
        # black color
        black_color = (0, 0, 0)
        # coordinates for play again button
        reset_btn = pygame.Rect(250, 300, 140, 50)
        # show reset button
        pygame.draw.rect(self.screen, black_color, reset_btn)

        # white color
        white_color = (255, 255, 255)
        # create fonts for texts
        big_font = pygame.font.SysFont("comicsansms", 50)
        small_font = pygame.font.SysFont("comicsansms", 20)

        # text to show winner
        text = winner + " wins!" 
        winner_text = big_font.render(text, False, black_color)

        # create text to be shown on the reset button
        reset_label = "Play Again"
        reset_btn_label = small_font.render(reset_label, True, white_color)

        # show winner text
        self.screen.blit(winner_text, 
                      ((self.screen.get_width() - winner_text.get_width()) // 2, 
                      150))
        
        # show text on the reset button
        self.screen.blit(reset_btn_label, 
                      ((reset_btn.x + (reset_btn.width - reset_btn_label.get_width()) // 2, 
                      reset_btn.y + (reset_btn.height - reset_btn_label.get_height()) // 2)))

        # get pressed keys
        key_pressed = pygame.key.get_pressed()
        # 
        util = Utils()

        # check if left mouse button was clicked
        if util.left_click_event():
            # call function to get mouse event
            mouse_coords = util.get_mouse_event()

            # check if reset button was clicked
            if reset_btn.collidepoint(mouse_coords[0], mouse_coords[1]):
                # change button behavior as it is hovered
                pygame.draw.rect(self.screen, white_color, reset_btn, 3)
                
                # change menu flag
                self.menu_showed = False
            # check if enter or return key was pressed
            elif key_pressed[K_RETURN]:
                self.menu_showed = False
            # reset game
            self.chess.reset()
            # clear winner
            self.chess.winner = ""
