import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("جزیره گنج متروک")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)

# Load images (placeholder functions)
def load_image(name, size):
    surf = pygame.Surface(size)
    surf.fill(BROWN if "tree" in name else YELLOW if "coin" in name else BLUE)
    return surf

# Game assets
class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.weapon = None
        self.ammo = 0
        self.image = load_image("player", (40, 60))
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
        
    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Boundary checking
        if 0 <= new_x <= SCREEN_WIDTH - 40:
            self.x = new_x
        if 0 <= new_y <= SCREEN_HEIGHT - 60:
            self.y = new_y
            
        self.rect.x = self.x
        self.rect.y = self.y
        
    def shoot(self):
        if self.weapon and self.ammo > 0:
            self.ammo -= 1
            return Bullet(self.x + 20, self.y + 30, pygame.mouse.get_pos())
        return None
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, 40 * (self.health / self.max_health), 5))

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.5, 2.0)
        self.health = 30
        self.damage = 10
        self.image = load_image("enemy", (40, 60))
        self.rect = pygame.Rect(self.x, self.y, 40, 60)
        
    def update(self, player_x, player_y):
        # Simple AI: move toward player
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        self.x += (dx / dist) * self.speed
        self.y += (dy / dist) * self.speed
        
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        
        # Health bar
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, 40 * (self.health / 30), 5))

class Bullet:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y
        self.speed = 10
        self.damage = 25
        
        # Calculate direction
        dx = target_pos[0] - x
        dy = target_pos[1] - y
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        self.dx = (dx / dist) * self.speed
        self.dy = (dy / dist) * self.speed
        
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = self.x
        self.rect.y = self.y
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 5)

class Treasure:
    def __init__(self, x, y, treasure_type):
        self.x = x
        self.y = y
        self.type = treasure_type  # "gold", "weapon", "health"
        self.collected = False
        
        if treasure_type == "gold":
            self.image = load_image("coin", (30, 30))
            self.value = random.randint(10, 100)
        elif treasure_type == "weapon":
            self.image = load_image("weapon", (30, 30))
            self.value = "pistol"
        else:  # health
            self.image = load_image("health", (30, 30))
            self.value = 25
            
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        
    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)

# Game setup
player = Player()
enemies = []
treasures = []
bullets = []
obstacles = []
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)

# Create obstacles (trees, rocks, etc.)
for _ in range(20):
    obstacles.append(Obstacle(
        random.randint(0, SCREEN_WIDTH - 50),
        random.randint(0, SCREEN_HEIGHT - 50),
        random.randint(30, 80),
        random.randint(30, 80)
    ))

# Create treasures
for _ in range(15):
    treasure_type = random.choice(["gold", "gold", "gold", "weapon", "health"])
    treasures.append(Treasure(
        random.randint(50, SCREEN_WIDTH - 50),
        random.randint(50, SCREEN_HEIGHT - 50),
        treasure_type
    ))

# Create initial enemies
for _ in range(3):
    enemies.append(Enemy(
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT)
    ))

# Game loop
clock = pygame.time.Clock()
spawn_timer = 0

def draw_hud():
    score_text = font.render(f"score: {score}", True, WHITE)
    health_text = font.render(f"health: {player.health}", True, WHITE)
    ammo_text = font.render(f"armor: {player.ammo}", True, WHITE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(health_text, (10, 50))
    screen.blit(ammo_text, (10, 90))

running = True
while running:
    # Clear screen
    screen.fill((50, 50, 100))  # Dark blue background
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if event.button == 1:  # Left click
                bullet = player.shoot()
                if bullet:
                    bullets.append(bullet)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
                player = Player()
                enemies = []
                treasures = []
                bullets = []
                score = 0
                game_over = False
                
                # Recreate game objects
                for _ in range(3):
                    enemies.append(Enemy(
                        random.randint(0, SCREEN_WIDTH),
                        random.randint(0, SCREEN_HEIGHT)
                    ))
                
                for _ in range(15):
                    treasure_type = random.choice(["gold", "gold", "gold", "weapon", "health"])
                    treasures.append(Treasure(
                        random.randint(50, SCREEN_WIDTH - 50),
                        random.randint(50, SCREEN_HEIGHT - 50),
                        treasure_type
                    ))
    
    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
            
        player.move(dx, dy)
        
        # Check collision with obstacles
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.rect):
                # Simple collision response
                if dx > 0:  # Moving right
                    player.x = obstacle.rect.left - player.rect.width
                elif dx < 0:  # Moving left
                    player.x = obstacle.rect.right
                if dy > 0:  # Moving down
                    player.y = obstacle.rect.top - player.rect.height
                elif dy < 0:  # Moving up
                    player.y = obstacle.rect.bottom
                
                player.rect.x = player.x
                player.rect.y = player.y
        
        # Spawn enemies periodically
        spawn_timer += 1
        if spawn_timer >= 180:  # Every 3 seconds
            spawn_timer = 0
            enemies.append(Enemy(
                random.choice([-50, SCREEN_WIDTH + 50]),
                random.randint(50, SCREEN_HEIGHT - 50)
            ))
        
        # Update enemies
        for enemy in enemies[:]:
            enemy.update(player.x, player.y)
            
            # Check collision with player
            if player.rect.colliderect(enemy.rect):
                player.health -= enemy.damage * 0.1  # Continuous damage
                if player.health <= 0:
                    game_over = True
        
        # Update bullets
        for bullet in bullets[:]:
            bullet.update()
            
            # Check if bullet is out of screen
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or 
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                bullets.remove(bullet)
                continue
                
            # Check collision with enemies
            for enemy in enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= bullet.damage
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        score += 50
                    break
        
        # Check treasure collection
        for treasure in treasures[:]:
            if not treasure.collected and player.rect.colliderect(treasure.rect):
                treasure.collected = True
                if treasure.type == "gold":
                    score += treasure.value
                elif treasure.type == "weapon":
                    player.weapon = treasure.value
                    player.ammo += 10
                else:  # health
                    player.health = min(player.max_health, player.health + treasure.value)
                
                treasures.remove(treasure)
                
                # Spawn new treasure occasionally
                if random.random() < 0.3:
                    treasures.append(Treasure(
                        random.randint(50, SCREEN_WIDTH - 50),
                        random.randint(50, SCREEN_HEIGHT - 50),
                        random.choice(["gold", "gold", "gold", "weapon", "health"])
                    ))
    
    # Drawing
    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)
    
    # Draw treasures
    for treasure in treasures:
        treasure.draw(screen)
    
    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw HUD
    draw_hud()
    
    # Draw game over screen
    if game_over:
        game_over_text = font.render("gameover! (R gameAgain", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                    SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()