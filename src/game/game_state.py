import pygame
import random
import math
from game.settings import *
from entities.player import Player
from entities.enemy import Enemy
from graphics.terrain_generator import TerrainGenerator
from graphics.character_generator import CharacterGenerator
from ui.shop import Shop
from ui.start_menu import StartMenu
from ui.hud import HUD

class GameState:
    def __init__(self):
        # Initialize generators
        self.terrain_gen = TerrainGenerator(tile_size=32)
        self.char_gen = CharacterGenerator(size=32)
        
        # Generate terrain
        self.terrain = self.terrain_gen.generate_chunk(
            width=SCREEN_WIDTH//32,
            height=SCREEN_HEIGHT//32,
            seed=random.randint(0, 1000)
        )
        
        # Create player with generated character sprite
        self.player = Player(character_sprite=self.char_gen.generate_character())
        self.enemies = []
        
        # Initialize UI elements
        self.shop = Shop()
        self.shop.set_player(self.player)  # Set player reference for shop
        self.start_menu = StartMenu(self.shop, self.player)
        self.hud = HUD()  # Initialize HUD
        
        # Game state
        self.state = GameStates.MENU
        self.score = 0
        self.current_round = STARTING_ROUND
        self.round_timer = ROUND_DURATION
        self.transition_timer = 0
        self.shop_timer = 0
        self.items_bought_this_round = 0
        
        # Bonfire system
        self.bonfire_cooldowns = {pos: 0 for pos in self.terrain_gen.bonfire_positions}
        
        # Difficulty tracking
        self.spawn_timer = 0
        self.current_spawn_delay = ENEMY_SPAWN_DELAY

    def start_new_round(self):
        """Initialize a new round with progressive difficulty"""
        self.round_timer = ROUND_DURATION
        self.enemies.clear()
        self.items_bought_this_round = 0
        
        # Calculate round completion reward
        round_reward = int(BASE_ROUND_REWARD * (1 + REWARD_SCALING * (self.current_round - 1)))
        self.player.add_money(round_reward)
        
        # Update spawn mechanics for new round
        self.current_spawn_delay = max(FPS, ENEMY_SPAWN_DELAY * (SPAWN_RATE_DECREASE ** (self.current_round - 1)))
        self.spawn_timer = 0
        
        # Spawn initial enemies
        num_enemies = min(MAX_ENEMIES, STARTING_ENEMIES + (self.current_round - 1) * ENEMY_COUNT_INCREASE)
        for _ in range(num_enemies):
            self.spawn_enemy()
            
        self.state = GameStates.PLAYING

    def enter_shop_phase(self):
        """Enter shopping phase between rounds"""
        self.state = GameStates.SHOPPING
        self.shop_timer = SHOP_TIME_LIMIT
        self.shop.refresh_items()  # Refresh shop items for new round
        
        # Heal player partially between rounds
        self.player.health = min(self.player.max_health, 
                               self.player.health + self.player.max_health * 0.3)

    def update(self):
        if self.state == GameStates.MENU:
            # Update start menu
            self.start_menu.update()
            if self.start_menu.should_start_round:
                self.start_new_round()
                
        elif self.state == GameStates.PLAYING:
            # Update game entities
            self.player.current_enemies = self.enemies
            self.player.update()
            self.update_enemies()
            self.handle_combat()
            
            # Update round timer
            self.round_timer -= 1
            if self.round_timer <= 0:
                self.current_round += 1
                self.enter_shop_phase()
            
            # Update bonfire cooldowns and particles
            for pos in self.bonfire_cooldowns:
                if self.bonfire_cooldowns[pos] > 0:
                    self.bonfire_cooldowns[pos] -= 1
            
            # Update particle effects
            self.terrain_gen.update_particles()
            
            # Check for bonfire healing
            self.check_bonfire_healing()
            
            # Remove dead enemies and spawn new ones
            self.enemies = [e for e in self.enemies if not e.is_dead]
            if len(self.enemies) < STARTING_ENEMIES + self.current_round - 1:
                self.spawn_enemy()
                
            # Progressive enemy spawning
            self.spawn_timer += 1
            if self.spawn_timer >= self.current_spawn_delay:
                self.spawn_timer = 0
                if len(self.enemies) < min(MAX_ENEMIES, STARTING_ENEMIES + (self.current_round - 1) * ENEMY_COUNT_INCREASE):
                    self.spawn_enemy()
                    
        elif self.state == GameStates.SHOPPING:
            # Update shop timer
            self.shop_timer -= 1
            
            # Handle shop interactions
            self.shop.update()
            
            # Handle purchase attempts
            if pygame.mouse.get_pressed()[0]:  # Left click
                if self.shop.selected_item:
                    if self.shop.purchase_selected_item(self.player):
                        self.items_bought_this_round += 1
            
            # Check if shopping phase should end
            if self.shop_timer <= 0 or self.items_bought_this_round >= ITEMS_PER_ROUND:
                self.start_new_round()
                
        elif self.state == GameStates.GAME_OVER:
            # Handle game over state
            pass

    def draw(self, screen):
        if self.state == GameStates.MENU:
            # Draw start menu
            self.start_menu.draw(screen)
            
        elif self.state == GameStates.PLAYING:
            # Draw game world
            screen.blit(self.terrain, (0, 0))
            
            # Draw bonfire effects
            for pos in self.bonfire_cooldowns:
                if self.bonfire_cooldowns[pos] > 0:
                    progress = self.bonfire_cooldowns[pos] / BONFIRE_COOLDOWN
                    radius = BONFIRE_HEAL_RADIUS * (1 - progress)
                    pygame.draw.circle(screen, (*ORANGE, 30), pos, int(radius), 1)
            
            # Draw entities
            self.player.draw(screen)
            for enemy in self.enemies:
                enemy.draw(screen)
                
            # Draw particle effects
            self.terrain_gen.draw_particles(screen)
            
            # Draw HUD
            self.hud.draw(screen, self.player, self.score, self.current_round, self.round_timer)
            
        elif self.state == GameStates.SHOPPING:
            # Draw shop interface
            self.shop.draw(screen)
            
        elif self.state == GameStates.GAME_OVER:
            self.draw_game_over(screen)

    def draw_hud(self, screen):
        font = pygame.font.Font(None, 36)
        
        # Draw score and round info
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        round_text = font.render(f'Round: {self.current_round}', True, WHITE)
        timer_text = font.render(f'Time: {self.round_timer // FPS}s', True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(round_text, (10, 50))
        screen.blit(timer_text, (10, 90))
        
        # Draw money
        money_text = font.render(f'Money: ${self.player.money}', True, GOLD)
        screen.blit(money_text, (SCREEN_WIDTH - 150, 10))
        
        # Draw health
        health_text = font.render(f'Health: {int(self.player.health)}/{int(self.player.max_health)}', True, GREEN)
        screen.blit(health_text, (SCREEN_WIDTH - 200, 50))

    def get_enemy_weights(self):
        """Get the spawn weights for the current round"""
        current_weights = None
        for round_num, weights in ENEMY_SPAWN_WEIGHTS:
            if self.current_round >= round_num:
                current_weights = weights
            else:
                break
        return current_weights or ENEMY_SPAWN_WEIGHTS[0][1]

    def spawn_enemy(self):
        """Spawn a new enemy with tier-based stats and progressive scaling"""
        if len(self.enemies) >= MAX_ENEMIES:
            return
            
        # Get spawn weights for current round
        weights = self.get_enemy_weights()
        
        # Select enemy tier based on weights
        total_weight = sum(weights.values())
        roll = random.uniform(0, total_weight)
        current_weight = 0
        selected_tier = None
        
        for tier, weight in weights.items():
            current_weight += weight
            if roll <= current_weight:
                selected_tier = tier
                break
        
        # Create enemy with tier stats
        enemy = Enemy()
        tier_stats = ENEMY_TIERS[selected_tier]
        
        # Set base stats from tier
        enemy.health = tier_stats["health"]
        enemy.max_health = tier_stats["health"]
        enemy.damage = tier_stats["damage"]
        enemy.speed = tier_stats["speed"]
        enemy.kill_reward = tier_stats["reward"]
        enemy.tier = selected_tier
        
        # Set monster type and sprite based on tier
        enemy.set_monster_type(selected_tier)
        
        # Apply round scaling
        round_factor = self.current_round - 1
        health_scale = 1 + (HEALTH_SCALING * round_factor)
        damage_scale = 1 + (DAMAGE_SCALING * round_factor)
        speed_scale = 1 + (SPEED_SCALING * round_factor)
        
        enemy.health *= health_scale
        enemy.max_health *= health_scale
        enemy.damage *= damage_scale
        enemy.speed *= speed_scale
        
        self.enemies.append(enemy)

    def update_enemies(self):
        """Update all enemies"""
        for enemy in self.enemies:
            enemy.update(self.player.rect.center)

    def handle_combat(self):
        """Handle combat between player and enemies"""
        # Check for enemy attacks
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if self.player.take_damage(enemy.damage):
                    # Player died
                    self.state = GameStates.GAME_OVER
                    return

        # Find closest enemy in range for auto-attack
        closest_enemy = None
        min_distance = float('inf')
        
        for enemy in self.enemies:
            if self.player.can_attack_enemy(enemy):
                dx = enemy.rect.centerx - self.player.rect.centerx
                dy = enemy.rect.centery - self.player.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
        
        # Auto-attack the closest enemy
        if closest_enemy:
            damage = self.player.attack()
            if damage > 0:  # If attack is ready
                if closest_enemy.take_damage(damage):
                    self.score += 1
                    self.player.add_money(ENEMY_KILL_REWARD)

    def check_bonfire_healing(self):
        """Check if player is near a bonfire and apply healing"""
        player_center = self.player.rect.center
        
        for bonfire_pos in self.terrain_gen.bonfire_positions:
            # Skip if bonfire is on cooldown
            if self.bonfire_cooldowns[bonfire_pos] > 0:
                continue
                
            # Check if player is in range
            dx = player_center[0] - bonfire_pos[0]
            dy = player_center[1] - bonfire_pos[1]
            distance = math.sqrt(dx * dx + dy * dy)
            
            if distance <= BONFIRE_HEAL_RADIUS:
                # Heal player and start cooldown
                self.player.heal(BONFIRE_HEAL_AMOUNT)
                self.bonfire_cooldowns[bonfire_pos] = BONFIRE_COOLDOWN
                # Create healing effect
                self.create_heal_effect(player_center)

    def create_heal_effect(self, position):
        """Create a visual healing effect"""
        effect_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw healing circles
        for radius in range(5, 20, 2):
            alpha = int(255 * (1 - radius/20))  # Fade out with distance
            pygame.draw.circle(effect_surface, (*GREEN, alpha), position, radius, 1)
            
        return effect_surface

    def draw_game_over(self, screen):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # More opaque
        screen.blit(overlay, (0, 0))
        
        # Game over text
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('Game Over!', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
        screen.blit(game_over_text, text_rect)
        
        # Score and round info
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f'Final Score: {self.score}', True, WHITE)
        round_text = score_font.render(f'Rounds Survived: {self.current_round}', True, WHITE)
        
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
        round_rect = round_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70))
        
        screen.blit(score_text, score_rect)
        screen.blit(round_text, round_rect)
        
        # Restart instruction
        inst_font = pygame.font.Font(None, 36)
        inst_text = inst_font.render('Press ESC to exit', True, WHITE)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150))
        screen.blit(inst_text, inst_rect) 