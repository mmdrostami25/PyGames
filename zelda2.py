import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zelda-like Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
class Player:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.radius = 20
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.projectiles = []
        self.shoot_cooldown = 0
        self.shoot_delay = 15  # frames
        
    def move(self, keys):
        if keys[pygame.K_a] and self.x > self.radius:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < SCREEN_WIDTH - self.radius:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > self.radius:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < SCREEN_HEIGHT - self.radius:
            self.y += self.speed
            
    def shoot(self, target_x, target_y):
        if self.shoot_cooldown == 0:
            angle = math.atan2(target_y - self.y, target_x - self.x)
            speed = 10
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.projectiles.append({
                'x': self.x,
                'y': self.y,
                'dx': dx,
                'dy': dy,
                'radius': 5
            })
            self.shoot_cooldown = self.shoot_delay
            # Play shoot sound (uncomment if you have a sound file)
            # pygame.mixer.Sound("shoot.wav").play()
    
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        # Update projectiles
        for proj in self.projectiles[:]:
            proj['x'] += proj['dx']
            proj['y'] += proj['dy']
            
            # Remove projectiles that go off-screen
            if (proj['x'] < 0 or proj['x'] > SCREEN_WIDTH or 
                proj['y'] < 0 or proj['y'] > SCREEN_HEIGHT):
                self.projectiles.remove(proj)
    
    def draw(self, screen):
        # Draw player
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_width = 50
        health_height = 5
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, RED, (self.x - health_width//2, self.y - 30, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.x - health_width//2, self.y - 30, int(health_width * health_ratio), health_height))
        
        # Draw projectiles
        for proj in self.projectiles:
            pygame.draw.circle(screen, YELLOW, (int(proj['x']), int(proj['y'])), proj['radius'])

# Enemy settings
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.speed = 1.5
        self.health = 30
        self.damage = 0.5
        
    def update(self, player_x, player_y):
        # Simple AI: move toward player
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        
    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_width = 30
        health_height = 3
        health_ratio = self.health / 30
        pygame.draw.rect(screen, RED, (self.x - health_width//2, self.y - 20, health_width, health_height))
        pygame.draw.rect(screen, GREEN, (self.x - health_width//2, self.y - 20, int(health_width * health_ratio), health_height))

# Item settings
class Item:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.radius = 10
        self.type = item_type  # "health" or "ammo"
        self.collected = False
        
    def draw(self, screen):
        if not self.collected:
            color = GREEN if self.type == "health" else YELLOW
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

# Game setup
player = Player()
enemies = []
items = []
score = 0
level = 1
spawn_timer = 0
game_over = False
font = pygame.font.SysFont(None, 36)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Clear screen
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
                player = Player()
                enemies = []
                items = []
                score = 0
                level = 1
                game_over = False
    
    if not game_over:
        # Player controls
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.update()
        
        # Spawn enemies
        spawn_timer += 1
        if spawn_timer >= 60 * (3 - min(level/10, 2)):  # Spawn rate increases with level
            spawn_timer = 0
            # Spawn from edges
            side = random.randint(0, 3)
            if side == 0:  # top
                x = random.randint(0, SCREEN_WIDTH)
                y = -20
            elif side == 1:  # right
                x = SCREEN_WIDTH + 20
                y = random.randint(0, SCREEN_HEIGHT)
            elif side == 2:  # bottom
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT + 20
            else:  # left
                x = -20
                y = random.randint(0, SCREEN_HEIGHT)
            enemies.append(Enemy(x, y))
        
        # Spawn items occasionally
        if random.random() < 0.005:
            item_type = "health" if random.random() < 0.7 else "ammo"
            items.append(Item(
                random.randint(20, SCREEN_WIDTH-20),
                random.randint(20, SCREEN_HEIGHT-20),
                item_type
            ))
        
        # Update enemies
        for enemy in enemies[:]:
            enemy.update(player.x, player.y)
            
            # Check collision with player
            dist = math.hypot(player.x - enemy.x, player.y - enemy.y)
            if dist < player.radius + enemy.radius:
                player.health -= enemy.damage
                if player.health <= 0:
                    game_over = True
            
            # Check collision with projectiles
            for proj in player.projectiles[:]:
                proj_dist = math.hypot(proj['x'] - enemy.x, proj['y'] - enemy.y)
                if proj_dist < proj['radius'] + enemy.radius:
                    enemy.health -= 10
                    if proj in player.projectiles:
                        player.projectiles.remove(proj)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += 10
                        # Chance to level up after killing enough enemies
                        if score >= level * 50:
                            level += 1
                            player.max_health += 10
                            player.health = player.max_health
                    break
        
        # Check item collection
        for item in items[:]:
            if not item.collected:
                dist = math.hypot(player.x - item.x, player.y - item.y)
                if dist < player.radius + item.radius:
                    item.collected = True
                    if item.type == "health":
                        player.health = min(player.max_health, player.health + 20)
                    else:  # ammo
                        player.shoot_delay = max(5, player.shoot_delay - 2)
                    items.remove(item)
    
    # Drawing
    # Draw items
    for item in items:
        item.draw(screen)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("GAME OVER - Press R to restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                    SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()