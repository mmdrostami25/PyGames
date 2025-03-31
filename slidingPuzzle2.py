import pygame
import random

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 3
TILE_SIZE = WIDTH // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")

# ایجاد صفحه
tiles = [(x + y * GRID_SIZE) for y in range(GRID_SIZE) for x in range(GRID_SIZE)]
tiles[-1] = -1  # جای خالی
random.shuffle(tiles)

def draw():
    screen.fill((0, 0, 0))
    for i, num in enumerate(tiles):
        if num == -1: continue
        x = (i % GRID_SIZE) * TILE_SIZE
        y = (i // GRID_SIZE) * TILE_SIZE
        pygame.draw.rect(screen, (255, 255, 255), (x, y, TILE_SIZE-2, TILE_SIZE-2))
        font = pygame.font.Font(None, 40)
        text = font.render(str(num+1), True, (0, 0, 0))
        screen.blit(text, (x + TILE_SIZE//3, y + TILE_SIZE//3))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # منطق حرکت کاشی‌ها
            pass
            
    draw()
    pygame.display.flip()

pygame.quit()