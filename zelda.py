import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adventure Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player settings
player_x = 400
player_y = 300
player_speed = 5
player_health = 100
player_attack_cooldown = 0

# Items
items = [{"x": 100, "y": 200, "type": "key", "collected": False},
         {"x": 500, "y": 400, "type": "potion", "collected": False}]

# Enemies
enemies = [{"x": 300, "y": 200, "health": 30, "speed": 2}]

# Game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, 30, 30))

def draw_item(x, y, item_type):
    color = GREEN if item_type == "potion" else WHITE
    pygame.draw.rect(screen, color, (x, y, 20, 20))

def draw_enemy(x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 30, 30))

running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_attack_cooldown == 0:
                # Attack logic
                player_attack_cooldown = 20
                for enemy in enemies:
                    if abs(player_x - enemy["x"]) < 40 and abs(player_y - enemy["y"]) < 40:
                        enemy["health"] -= 10
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - 30:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - 30:
        player_y += player_speed
    
    # Item collection
    for item in items:
        if not item["collected"]:
            if (abs(player_x - item["x"]) < 25 and abs(player_y - item["y"]) < 25):
                item["collected"] = True
                if item["type"] == "potion":
                    player_health = min(100, player_health + 20)
    
    # Enemy AI (simple follow)
    for enemy in enemies:
        if enemy["x"] < player_x:
            enemy["x"] += enemy["speed"]
        elif enemy["x"] > player_x:
            enemy["x"] -= enemy["speed"]
        if enemy["y"] < player_y:
            enemy["y"] += enemy["speed"]
        elif enemy["y"] > player_y:
            enemy["y"] -= enemy["speed"]
        
        # Enemy collision with player
        if (abs(player_x - enemy["x"]) < 30 and abs(player_y - enemy["y"]) < 30):
            player_health -= 0.5
    
    # Drawing
    for item in items:
        if not item["collected"]:
            draw_item(item["x"], item["y"], item["type"])
    
    for enemy in enemies:
        if enemy["health"] > 0:
            draw_enemy(enemy["x"], enemy["y"])
    
    draw_player(player_x, player_y)
    
    # UI
    health_text = font.render(f"Health: {int(player_health)}", True, WHITE)
    screen.blit(health_text, (10, 10))
    
    # Attack cooldown
    if player_attack_cooldown > 0:
        player_attack_cooldown -= 1
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()