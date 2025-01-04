import json
import os
import pygame
from game.settings import *

class SettingsManager:
    def __init__(self):
        self.settings = {
            "graphics": {
                "resolution": (1280, 720),
                "fullscreen": False,
                "vsync": True,
                "effects_quality": "High"
            },
            "sound": {
                "master_volume": 1.0,
                "music_volume": 0.7,
                "effects_volume": 0.8
            },
            "controls": {
                "mouse_sensitivity": 1.0,
                "key_bindings": {
                    "move_up": pygame.K_w,
                    "move_down": pygame.K_s,
                    "move_left": pygame.K_a,
                    "move_right": pygame.K_d,
                    "attack": pygame.BUTTON_LEFT,
                    "special": pygame.BUTTON_RIGHT,
                    "dash": pygame.K_SPACE,
                    "inventory": pygame.K_i,
                    "pause": pygame.K_ESCAPE
                }
            },
            "gameplay": {
                "difficulty": "Normal",
                "tutorial_tips": True,
                "combat_numbers": True,
                "screen_shake": True
            }
        }
        
        self.load_settings()
        
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    saved_settings = json.load(f)
                    # Update settings while preserving defaults for new settings
                    self.update_dict_recursive(self.settings, saved_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def save_settings(self):
        """Save settings to file"""
        try:
            with open("settings.json", "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def update_dict_recursive(self, target, source):
        """Update dictionary recursively while preserving structure"""
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    self.update_dict_recursive(target[key], value)
                else:
                    target[key] = value
                    
    def get_setting(self, category, setting):
        """Get a specific setting value"""
        try:
            return self.settings[category][setting]
        except KeyError:
            print(f"Setting not found: {category}.{setting}")
            return None
            
    def set_setting(self, category, setting, value):
        """Set a specific setting value"""
        try:
            self.settings[category][setting] = value
            self.save_settings()
            return True
        except KeyError:
            print(f"Setting not found: {category}.{setting}")
            return False
            
    def apply_graphics_settings(self):
        """Apply current graphics settings"""
        resolution = self.settings["graphics"]["resolution"]
        fullscreen = self.settings["graphics"]["fullscreen"]
        
        flags = pygame.FULLSCREEN if fullscreen else 0
        if self.settings["graphics"]["vsync"]:
            flags |= pygame.DOUBLEBUF
            
        return pygame.display.set_mode(resolution, flags)
        
    def apply_sound_settings(self, sound_manager):
        """Apply current sound settings"""
        sound_manager.set_master_volume(self.settings["sound"]["master_volume"])
        sound_manager.set_music_volume(self.settings["sound"]["music_volume"])
        sound_manager.set_effects_volume(self.settings["sound"]["effects_volume"])
        
    def get_key_binding(self, action):
        """Get the key binding for a specific action"""
        try:
            return self.settings["controls"]["key_bindings"][action]
        except KeyError:
            print(f"Key binding not found for action: {action}")
            return None
            
    def set_key_binding(self, action, key):
        """Set the key binding for a specific action"""
        try:
            self.settings["controls"]["key_bindings"][action] = key
            self.save_settings()
            return True
        except KeyError:
            print(f"Invalid action for key binding: {action}")
            return False
            
    def reset_to_defaults(self, category=None):
        """Reset settings to defaults"""
        default_settings = {
            "graphics": {
                "resolution": (1280, 720),
                "fullscreen": False,
                "vsync": True,
                "effects_quality": "High"
            },
            "sound": {
                "master_volume": 1.0,
                "music_volume": 0.7,
                "effects_volume": 0.8
            },
            "controls": {
                "mouse_sensitivity": 1.0,
                "key_bindings": {
                    "move_up": pygame.K_w,
                    "move_down": pygame.K_s,
                    "move_left": pygame.K_a,
                    "move_right": pygame.K_d,
                    "attack": pygame.BUTTON_LEFT,
                    "special": pygame.BUTTON_RIGHT,
                    "dash": pygame.K_SPACE,
                    "inventory": pygame.K_i,
                    "pause": pygame.K_ESCAPE
                }
            },
            "gameplay": {
                "difficulty": "Normal",
                "tutorial_tips": True,
                "combat_numbers": True,
                "screen_shake": True
            }
        }
        
        if category:
            if category in self.settings:
                self.settings[category] = default_settings[category].copy()
            else:
                print(f"Invalid settings category: {category}")
                return False
        else:
            self.settings = default_settings.copy()
            
        self.save_settings()
        return True 