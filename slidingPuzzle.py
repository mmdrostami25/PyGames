import pygame
import random

# تنظیمات پنجره
WIDTH = 400
HEIGHT = 400
TILE_SIZE = 100

# رنگها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")

# ایجاد صفحه پازل
tiles = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
empty_pos = (2, 2)

def draw_board():
    for i in range(3):
        for j in range(3):
            if tiles[i][j] != 0:
                pygame.draw.rect(screen, WHITE, (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE-2, TILE_SIZE-2))
                font = pygame.font.Font(None, 50)
                text = font.render(str(tiles[i][j]), True, BLACK)
                screen.blit(text, (j*TILE_SIZE + 35, i*TILE_SIZE + 30))

def move_tile(pos):
    global empty_pos
    i, j = pos
    if ((abs(i - empty_pos[0]) == 1 and j == empty_pos[1]) or 
        (abs(j - empty_pos[1]) == 1 and i == empty_pos[0])):
        tiles[empty_pos[0]][empty_pos[1]] = tiles[i][j]
        tiles[i][j] = 0
        empty_pos = (i, j)

# Shuffle tiles
for _ in range(100):
    moves = []
    if empty_pos[0] > 0: moves.append((empty_pos[0]-1, empty_pos[1]))
    if empty_pos[0] < 2: moves.append((empty_pos[0]+1, empty_pos[1]))
    if empty_pos[1] > 0: moves.append((empty_pos[0], empty_pos[1]-1))
    if empty_pos[1] < 2: moves.append((empty_pos[0], empty_pos[1]+1))
    move_tile(random.choice(moves))

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = y // TILE_SIZE
            j = x // TILE_SIZE
            move_tile((i, j))
    
    draw_board()
    pygame.display.update()

pygame.quit()