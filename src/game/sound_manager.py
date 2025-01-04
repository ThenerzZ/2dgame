import pygame
import numpy as np
import math

class SoundManager:
    def __init__(self, settings_manager):
        pygame.mixer.init(44100, -16, 2, 512)
        self.settings_manager = settings_manager
        self.sounds = {}
        self.create_sounds()
        
    def create_sounds(self):
        """Create all game sounds programmatically"""
        # Menu sounds
        self.sounds["menu_select"] = self.create_menu_select_sound()
        self.sounds["menu_back"] = self.create_menu_back_sound()
        self.sounds["menu_confirm"] = self.create_menu_confirm_sound()
        
        # Combat sounds
        self.sounds["player_hit"] = self.create_hit_sound()
        self.sounds["enemy_hit"] = self.create_enemy_hit_sound()
        self.sounds["player_death"] = self.create_death_sound()
        self.sounds["enemy_death"] = self.create_enemy_death_sound()
        
        # Item sounds
        self.sounds["pickup_gold"] = self.create_pickup_sound()
        self.sounds["buy_item"] = self.create_buy_sound()
        
        # Ambient sounds
        self.sounds["level_up"] = self.create_level_up_sound()
        self.sounds["game_over"] = self.create_game_over_sound()
        
    def create_sine_wave(self, frequency, duration, volume=0.5):
        """Create a sine wave sound"""
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        wave = np.sin(2 * np.pi * frequency * t)
        wave = (wave * volume * 32767).astype(np.int16)
        # Convert to stereo by duplicating the wave
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_menu_select_sound(self):
        """Create a dark, ethereal menu selection sound"""
        duration = 0.15
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Lower frequency for darker tone
        wave = np.sin(2 * np.pi * 220 * t) + 0.3 * np.sin(2 * np.pi * 330 * t)
        wave = wave * np.exp(-4 * t)
        wave = (wave * 24000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_menu_back_sound(self):
        """Create an eerie menu back sound"""
        duration = 0.2
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        freq = 180 * (1 + 0.1 * np.sin(2 * np.pi * 5 * t))  # Add slight wobble
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-3 * t)
        wave = (wave * 24000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_menu_confirm_sound(self):
        """Create a dark, resonant confirmation sound"""
        duration = 0.3
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Deeper frequencies with harmonics
        wave = np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 225 * t)
        wave += 0.25 * np.sin(2 * np.pi * 300 * t)
        wave = wave * (1 - np.exp(-5 * t))
        wave = (wave * 20000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_hit_sound(self):
        """Create a meaty, impactful hit sound"""
        duration = 0.15
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Mix noise with low frequency for impact
        noise = np.random.uniform(-0.7, 0.7, len(t))
        base = np.sin(2 * np.pi * 80 * t) * np.exp(-20 * t)
        wave = (noise + base) * np.exp(-15 * t)
        wave = (wave * 28000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_enemy_hit_sound(self):
        """Create a grotesque enemy hit sound"""
        duration = 0.2
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Dissonant frequencies for unsettling effect
        wave = np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 173 * t)
        wave *= np.exp(-10 * t)
        wave = (wave * 28000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_death_sound(self):
        """Create an echoing death sound"""
        duration = 0.8
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Falling pitch with echo effect
        freq = 200 * np.exp(-2 * t)
        wave = np.sin(2 * np.pi * freq * t)
        # Add echo
        echo = np.roll(wave, int(0.1 * sample_rate)) * 0.5
        wave = (wave + echo) * np.exp(-2 * t)
        wave = (wave * 28000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_enemy_death_sound(self):
        """Create a demonic enemy death sound"""
        duration = 0.4
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Descending growl effect
        freq = 120 * np.exp(-3 * t)
        wave = np.sin(2 * np.pi * freq * t)
        # Add distortion
        wave = np.clip(wave * 1.5, -1, 1) * np.exp(-4 * t)
        wave = (wave * 28000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_pickup_sound(self):
        """Create a mystical pickup sound"""
        duration = 0.2
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Ethereal ascending frequencies
        wave = np.sin(2 * np.pi * (300 + 200 * t) * t)
        wave += 0.3 * np.sin(2 * np.pi * (450 + 300 * t) * t)
        wave = wave * (1 - np.exp(-10 * t))
        wave = (wave * 20000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_buy_sound(self):
        """Create a mystical item purchase sound"""
        duration = 0.3
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Resonant harmonics
        wave = np.sin(2 * np.pi * 200 * t) + 0.5 * np.sin(2 * np.pi * 300 * t)
        wave += 0.25 * np.sin(2 * np.pi * 400 * t)
        wave = wave * (1 - np.exp(-8 * t))
        wave = (wave * 20000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_level_up_sound(self):
        """Create an ominous level up sound"""
        duration = 0.6
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Rising dark chord
        wave = np.sin(2 * np.pi * (150 + 100 * t) * t)
        wave += 0.5 * np.sin(2 * np.pi * (225 + 150 * t) * t)
        wave += 0.25 * np.sin(2 * np.pi * (300 + 200 * t) * t)
        wave = wave * (1 - np.exp(-5 * t))
        wave = (wave * 24000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def create_game_over_sound(self):
        """Create a haunting game over sound"""
        duration = 1.5
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Descending dissonant chord with echo
        freq1 = 200 * np.exp(-1 * t)
        freq2 = 150 * np.exp(-1 * t)
        wave = np.sin(2 * np.pi * freq1 * t) + 0.5 * np.sin(2 * np.pi * freq2 * t)
        # Add echo effect
        echo = np.roll(wave, int(0.2 * sample_rate)) * 0.3
        wave = (wave + echo) * np.exp(-1 * t)
        wave = (wave * 28000).astype(np.int16)
        stereo = np.array([wave, wave]).T.copy()
        return pygame.sndarray.make_sound(stereo)
        
    def play_sound(self, sound_name):
        """Play a sound with the current volume settings"""
        if sound_name in self.sounds:
            volume = self.settings_manager.get_setting("sound", "effects_volume")
            master_volume = self.settings_manager.get_setting("sound", "master_volume")
            self.sounds[sound_name].set_volume(volume * master_volume)
            self.sounds[sound_name].play() 