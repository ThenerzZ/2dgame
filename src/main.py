import pygame
import sys
from game.game_state import GameState
from ui.main_menu import MainMenu
from game.settings import *
from game.settings_manager import SettingsManager

class Game:
    def __init__(self):
        pygame.init()
        
        # Initialize display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dark Fantasy Game")
        
        # Initialize game states
        self.settings_manager = SettingsManager()
        self.game_state = None
        self.main_menu = MainMenu()
        self.current_state = GameStates.MENU
        self.clock = pygame.time.Clock()
        self.paused_game_state = None  # Store game state when paused
        
    def run(self):
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # Handle menu input when in menu state
                if self.current_state == GameStates.MENU:
                    self.main_menu.handle_input(event)
                    if self.main_menu.should_start_game:
                        self.current_state = GameStates.PLAYING
                        if self.main_menu.continue_game and self.paused_game_state:
                            # Restore the paused game state
                            self.game_state = self.paused_game_state
                            self.paused_game_state = None
                            # Make sure the game state is set to PLAYING
                            self.game_state.state = GameStates.PLAYING
                        else:
                            # Create new game state
                            self.game_state = GameState()
                            self.paused_game_state = None
                        self.main_menu.should_start_game = False
                        
                # Handle game input when playing
                elif self.current_state == GameStates.PLAYING and self.game_state:
                    self.game_state.handle_input(event)
                    # Check if game state wants to return to menu
                    if self.game_state.state == GameStates.MENU:
                        self.current_state = GameStates.MENU
                        # Store the current game state before switching to menu
                        self.paused_game_state = self.game_state
                        self.game_state = None
                        self.main_menu.reset(has_game_to_continue=True)
            
            # Update
            if self.current_state == GameStates.MENU:
                self.main_menu.update()
            elif self.current_state == GameStates.PLAYING and self.game_state:
                self.game_state.update()
                
                # Check for game over
                if self.game_state.state == GameStates.GAME_OVER:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.current_state = GameStates.MENU
                        self.game_state = None
                        self.paused_game_state = None  # Clear paused game on game over
                        self.main_menu.reset(has_game_to_continue=False)
            
            # Draw
            self.screen.fill(UI_COLORS["BACKGROUND"])
            
            if self.current_state == GameStates.MENU:
                self.main_menu.draw(self.screen)
            elif self.current_state == GameStates.PLAYING and self.game_state:
                self.game_state.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 