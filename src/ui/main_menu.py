import pygame
import math
import random
import sys
from game.settings import *

class MainMenu:
    def __init__(self, settings_manager):
        self.current_menu = "MAIN"
        self.selected_option = 0
        self.transition_alpha = 255
        self.fade_out = False
        self.should_start_game = False
        self.continue_game = False
        self.has_game_to_continue = False
        self.settings_manager = settings_manager
        
        # Animation variables
        self.animation_time = 0
        self.hover_scale = 1.0
        self.particles = []
        self.background_offset = 0  # Initialize background offset
        
        # Initialize fonts
        self.title_font = pygame.font.Font(None, UI_TITLE_SIZE)
        self.option_font = pygame.font.Font(None, UI_TEXT_SIZE)
        
        # Load and scale background
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(UI_COLORS["BACKGROUND"])
        
        # Create decorative elements
        self.create_decorative_elements()
        
    def create_decorative_elements(self):
        """Create decorative UI elements like borders and patterns"""
        self.border_pattern = []
        for i in range(8):  # Create 8 corner pieces
            angle = i * (math.pi / 4)
            x = math.cos(angle) * 100
            y = math.sin(angle) * 100
            self.border_pattern.append((x, y))
            
    def create_particle(self, pos):
        """Create a decorative particle effect"""
        return {
            'pos': list(pos),
            'vel': [random.uniform(-1, 1), random.uniform(-2, 0)],
            'lifetime': random.randint(30, 60),
            'size': random.randint(2, 4),
            'color': UI_COLORS["ACCENT"]
        }
        
    def update(self):
        # Update animation time
        self.animation_time += 1
        self.background_offset = (self.background_offset + 0.5) % SCREEN_WIDTH
        
        # Update particles
        for particle in self.particles[:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
                
        # Add new particles occasionally
        if random.random() < 0.1:
            x = random.randint(0, SCREEN_WIDTH)
            self.particles.append(self.create_particle((x, SCREEN_HEIGHT - 50)))
            
        # Handle fade transition
        if self.fade_out:
            self.transition_alpha = min(255, self.transition_alpha + 5)
        else:
            self.transition_alpha = max(0, self.transition_alpha - 5)
            
    def draw(self, screen):
        # Draw background with parallax effect
        screen.fill(UI_COLORS["BACKGROUND"])
        
        # Draw decorative patterns
        self.draw_decorative_patterns(screen)
        
        # Draw title
        title_text = "Dark Fantasy Game"
        title_surf = self.title_font.render(title_text, True, UI_COLORS["ACCENT"])
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        
        # Add glow effect to title
        glow_surf = pygame.Surface((title_surf.get_width() + 20, title_surf.get_height() + 20), pygame.SRCALPHA)
        for radius in range(10, 0, -2):
            color = (*UI_COLORS["ACCENT"][:3], 5)
            pygame.draw.rect(glow_surf, color, 
                           (10-radius, 10-radius, 
                            title_surf.get_width() + radius*2, 
                            title_surf.get_height() + radius*2),
                           border_radius=radius)
        screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_surf, title_rect)
        
        # Draw menu options
        option_y = SCREEN_HEIGHT//2
        menu_options = MENU_OPTIONS.get(self.current_menu, [])
        for i, option in enumerate(menu_options):
            selected = i == self.selected_option
            self.draw_menu_option(screen, option, option_y, selected)
            option_y += UI_BUTTON_HEIGHT + 10
            
        # Draw settings values if in settings menus
        if self.current_menu in ["GRAPHICS", "SOUND", "CONTROLS", "GAMEPLAY"]:
            self.draw_settings_values(screen)
            
        # Draw particles
        for particle in self.particles:
            alpha = int((particle['lifetime'] / 60) * 255)
            color = (*particle['color'][:3], alpha)
            pygame.draw.circle(screen, color, 
                             [int(particle['pos'][0]), int(particle['pos'][1])],
                             particle['size'])
            
        # Draw fade overlay
        if self.transition_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.transition_alpha)
            screen.blit(fade_surf, (0, 0))
            
    def draw_menu_option(self, screen, text, y, selected):
        # Calculate hover effect
        hover_offset = math.sin(self.animation_time * 0.05) * 3 if selected else 0
        scale = 1.1 if selected else 1.0
        
        # Create text surface
        color = UI_COLORS["ACCENT"] if selected else UI_COLORS["TEXT"]
        # Gray out continue option if not available
        if text == "Continue" and not self.has_game_to_continue:
            color = UI_COLORS["TEXT_DARK"]
            
        text_surf = self.option_font.render(text, True, color)
        text_surf = pygame.transform.scale(text_surf, 
                                         (int(text_surf.get_width() * scale),
                                          int(text_surf.get_height() * scale)))
        
        # Position text
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH//2, y + hover_offset))
        
        # Draw selection indicator
        if selected and (text != "Continue" or self.has_game_to_continue):
            # Draw glowing border
            border_rect = text_rect.inflate(40, 20)
            for offset in range(4, 0, -1):
                color = (*UI_COLORS["ACCENT"][:3], 50)
                pygame.draw.rect(screen, color, border_rect.inflate(offset*2, offset*2),
                               2, border_radius=10)
            
            # Draw side decorations
            decoration_length = 20
            pygame.draw.line(screen, UI_COLORS["ACCENT"],
                           (text_rect.left - 30, text_rect.centery),
                           (text_rect.left - 30 + decoration_length, text_rect.centery),
                           2)
            pygame.draw.line(screen, UI_COLORS["ACCENT"],
                           (text_rect.right + 30, text_rect.centery),
                           (text_rect.right + 30 - decoration_length, text_rect.centery),
                           2)
            
        screen.blit(text_surf, text_rect)
        
    def draw_settings_values(self, screen):
        """Draw current values for settings options"""
        if self.current_menu == "GRAPHICS":
            resolution = self.settings_manager.get_setting("graphics", "resolution")
            fullscreen = self.settings_manager.get_setting("graphics", "fullscreen")
            vsync = self.settings_manager.get_setting("graphics", "vsync")
            effects = self.settings_manager.get_setting("graphics", "effects_quality")
            values = [
                f"{resolution[0]}x{resolution[1]}",
                "On" if fullscreen else "Off",
                "On" if vsync else "Off",
                effects,
                ""  # Back button has no value
            ]
        elif self.current_menu == "SOUND":
            master = self.settings_manager.get_setting("sound", "master_volume")
            music = self.settings_manager.get_setting("sound", "music_volume")
            effects = self.settings_manager.get_setting("sound", "effects_volume")
            values = [
                f"{int(master * 100)}%",
                f"{int(music * 100)}%",
                f"{int(effects * 100)}%",
                ""  # Back button has no value
            ]
        elif self.current_menu == "GAMEPLAY":
            difficulty = self.settings_manager.get_setting("gameplay", "difficulty")
            tutorial = self.settings_manager.get_setting("gameplay", "tutorial_tips")
            combat_nums = self.settings_manager.get_setting("gameplay", "combat_numbers")
            screen_shake = self.settings_manager.get_setting("gameplay", "screen_shake")
            values = [
                difficulty,
                "On" if tutorial else "Off",
                "On" if combat_nums else "Off",
                "On" if screen_shake else "Off",
                ""  # Back button has no value
            ]
        else:
            return
            
        # Draw values
        for i, value in enumerate(values):
            if value:  # Don't draw empty values (for Back button)
                text_surf = self.option_font.render(value, True, UI_COLORS["TEXT_DARK"])
                text_rect = text_surf.get_rect(
                    midleft=(SCREEN_WIDTH//2 + 150, 
                            SCREEN_HEIGHT//2 + i * (UI_BUTTON_HEIGHT + 10))
                )
                screen.blit(text_surf, text_rect)
        
    def draw_decorative_patterns(self, screen):
        # Draw corner decorations
        corner_size = 100
        for corner in [(0, 0), (SCREEN_WIDTH, 0), 
                      (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)]:
            points = []
            for i in range(4):
                angle = i * (math.pi / 2) + (math.pi / 4)
                x = corner[0] + math.cos(angle) * corner_size
                y = corner[1] + math.sin(angle) * corner_size
                points.append((x, y))
            pygame.draw.lines(screen, UI_COLORS["BORDER"], True, points, 2)
            
        # Draw animated border lines
        border_offset = (self.animation_time * 2) % 40
        for i in range(0, SCREEN_WIDTH, 40):
            alpha = abs(math.sin(self.animation_time * 0.02 + i * 0.01)) * 255
            color = (*UI_COLORS["BORDER"][:3], int(alpha))
            pygame.draw.line(screen, color,
                           (i - border_offset, 0),
                           (i - border_offset + 20, 0), 2)
            pygame.draw.line(screen, color,
                           (i - border_offset, SCREEN_HEIGHT),
                           (i - border_offset + 20, SCREEN_HEIGHT), 2)
            
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(MENU_OPTIONS[self.current_menu])
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(MENU_OPTIONS[self.current_menu])
            elif event.key == pygame.K_RETURN:
                self.select_current_option()
            elif event.key == pygame.K_ESCAPE and self.current_menu != "MAIN":
                self.current_menu = "MAIN"
                self.selected_option = 0
                
    def select_current_option(self):
        selected = MENU_OPTIONS[self.current_menu][self.selected_option]
        
        if self.current_menu == "MAIN":
            if selected == "Continue" and self.has_game_to_continue:
                self.fade_out = True
                self.should_start_game = True
                self.continue_game = True
            elif selected == "New Game":
                self.fade_out = True
                self.should_start_game = True
                self.continue_game = False
            elif selected == "Settings":
                self.current_menu = "SETTINGS"
                self.selected_option = 0
            elif selected == "Exit":
                pygame.quit()
                sys.exit()
        elif self.current_menu == "SETTINGS":
            if selected == "Back":
                self.current_menu = "MAIN"
            else:
                self.current_menu = selected.upper()
            self.selected_option = 0
        elif selected == "Back":
            self.current_menu = "SETTINGS"
            self.selected_option = 0
        else:
            # Handle settings changes
            self.handle_setting_change(selected) 

    def handle_setting_change(self, setting):
        """Handle changes to settings values"""
        if self.current_menu == "GRAPHICS":
            if setting == "Resolution":
                resolutions = ["1280x720", "1920x1080", "2560x1440"]
                current = self.settings_manager.get_setting("graphics", "resolution")
                current_str = f"{current[0]}x{current[1]}"
                current_idx = resolutions.index(current_str)
                next_res = resolutions[(current_idx + 1) % len(resolutions)]
                width, height = map(int, next_res.split('x'))
                self.settings_manager.set_setting("graphics", "resolution", (width, height))
                
            elif setting == "Fullscreen":
                current = self.settings_manager.get_setting("graphics", "fullscreen")
                self.settings_manager.set_setting("graphics", "fullscreen", not current)
                
            elif setting == "VSync":
                current = self.settings_manager.get_setting("graphics", "vsync")
                self.settings_manager.set_setting("graphics", "vsync", not current)
                
            elif setting == "Effects Quality":
                qualities = ["Low", "Medium", "High", "Ultra"]
                current = self.settings_manager.get_setting("graphics", "effects_quality")
                current_idx = qualities.index(current)
                next_quality = qualities[(current_idx + 1) % len(qualities)]
                self.settings_manager.set_setting("graphics", "effects_quality", next_quality)
                
        elif self.current_menu == "SOUND":
            if setting == "Master Volume":
                current = int(self.settings_manager.get_setting("sound", "master_volume") * 100)
                next_value = (current + 10) % 110
                self.settings_manager.set_setting("sound", "master_volume", next_value / 100)
                
            elif setting == "Music Volume":
                current = int(self.settings_manager.get_setting("sound", "music_volume") * 100)
                next_value = (current + 10) % 110
                self.settings_manager.set_setting("sound", "music_volume", next_value / 100)
                
            elif setting == "Effects Volume":
                current = int(self.settings_manager.get_setting("sound", "effects_volume") * 100)
                next_value = (current + 10) % 110
                self.settings_manager.set_setting("sound", "effects_volume", next_value / 100)
                
        elif self.current_menu == "GAMEPLAY":
            if setting == "Difficulty":
                difficulties = ["Easy", "Normal", "Hard", "Nightmare"]
                current = self.settings_manager.get_setting("gameplay", "difficulty")
                current_idx = difficulties.index(current)
                next_difficulty = difficulties[(current_idx + 1) % len(difficulties)]
                self.settings_manager.set_setting("gameplay", "difficulty", next_difficulty)
                
            elif setting == "Tutorial Tips":
                current = self.settings_manager.get_setting("gameplay", "tutorial_tips")
                self.settings_manager.set_setting("gameplay", "tutorial_tips", not current)
                
            elif setting == "Combat Numbers":
                current = self.settings_manager.get_setting("gameplay", "combat_numbers")
                self.settings_manager.set_setting("gameplay", "combat_numbers", not current)
                
            elif setting == "Screen Shake":
                current = self.settings_manager.get_setting("gameplay", "screen_shake")
                self.settings_manager.set_setting("gameplay", "screen_shake", not current)

    def reset(self, has_game_to_continue=False):
        """Reset menu state when returning from game"""
        self.current_menu = "MAIN"
        self.selected_option = 0
        self.transition_alpha = 0  # Start fully visible
        self.fade_out = False
        self.should_start_game = False
        self.continue_game = False
        self.has_game_to_continue = has_game_to_continue
        self.animation_time = 0 