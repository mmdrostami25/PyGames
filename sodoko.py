import pygame

pygame.init()

# تنظیمات
WIDTH = 540
HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# رنگها
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (200,200,200)
BLUE = (0,0,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# تخته نمونه
board = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]

selected = None

def draw_grid():
    for i in range(GRID_SIZE+1):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i*CELL_SIZE, 0), (i*CELL_SIZE, HEIGHT-60), thickness)

def draw_numbers():
    font = pygame.font.Font(None, 40)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, BLACK)
                screen.blit(text, (j*CELL_SIZE+20, i*CELL_SIZE+15))

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if y < HEIGHT-60:
                selected = (y//CELL_SIZE, x//CELL_SIZE)
        if event.type == pygame.KEYDOWN and selected:
            if event.unicode.isdigit():
                num = int(event.unicode)
                board[selected[0]][selected[1]] = num
    
    draw_grid()
    draw_numbers()
    
    if selected:
        pygame.draw.rect(screen, BLUE, (selected[1]*CELL_SIZE, selected[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    
    pygame.display.update()

pygame.quit()