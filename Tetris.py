import pygame
import random
import time

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 700
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20
TOP_LEFT_X = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2
TOP_LEFT_Y = HEIGHT - (GRID_HEIGHT * GRID_SIZE) - 50

COLORS = [
    (0, 0, 0),
    (255, 0, 0),    # قرمز
    (0, 150, 255),  # آبی
    (0, 255, 0),    # سبز
    (255, 255, 0),  # زرد
    (255, 165, 0),  # نارنجی
    (128, 0, 128),  # بنفش
    (255, 192, 203) # صورتی (بمب)
]

SHAPES = [
    [[1, 1, 1, 1]],                             
    [[1, 1], [1, 1]],                           
    [[0, 1, 0], [1, 1, 1]],                     
    [[1, 0], [1, 0], [1, 1]],                   
    [[0, 1], [0, 1], [1, 1]],                   
    [[1, 1, 0], [0, 1, 1]],                     
    [[0, 1, 1], [1, 1, 0]],                     
    [[7, 7], [7, 7]]                            
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.level = 1
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        if random.randint(1, 10) == 1:
            return {
                'shape': SHAPES[-1],
                'color': 7,
                'x': GRID_WIDTH // 2 - 1,
                'y': 0
            }
        else:
            idx = random.randint(0, len(SHAPES)-2)
            return {
                'shape': SHAPES[idx],
                'color': idx + 1,
                'x': GRID_WIDTH // 2 - len(SHAPES[idx][0]) // 2,
                'y': 0
            }

    def check_collision(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    if not (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT):
                        return True
                    if self.grid[new_y][new_x]:
                        return True
        return False

    def move_piece(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False

    def rotate_piece(self):
        rotated = [list(row) for row in zip(*self.current_piece['shape'][::-1])]
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = rotated
        if self.check_collision(self.current_piece):
            self.current_piece['shape'] = old_shape

    def lock_piece(self):
        # قفل کردن قطعه در شبکه
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece['y'] + y
                    grid_x = self.current_piece['x'] + x
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        self.grid[grid_y][grid_x] = self.current_piece['color']

    def handle_bomb(self):
        # فعالسازی بمب
        if self.current_piece['color'] == 7:
            x, y = self.current_piece['x'], self.current_piece['y']
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if 0 <= x+i < GRID_WIDTH and 0 <= y+j < GRID_HEIGHT:
                        self.grid[y+j][x+i] = 0
            self.score += 500
            return True
        return False

    def clear_lines(self):
        # پاک کردن خطوط کامل
        lines_cleared = 0
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_cleared += 1
                del self.grid[y]
                self.grid.insert(0, [0]*GRID_WIDTH)
        return lines_cleared

def draw_grid(surface, game):
    # رسم شبکه و قطعات
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(TOP_LEFT_X + x*GRID_SIZE, TOP_LEFT_Y + y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, COLORS[game.grid[y][x]], rect)
            pygame.draw.rect(surface, (40,40,40), rect, 1)

    if game.current_piece:
        for y, row in enumerate(game.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        TOP_LEFT_X + (game.current_piece['x'] + x)*GRID_SIZE,
                        TOP_LEFT_Y + (game.current_piece['y'] + y)*GRID_SIZE,
                        GRID_SIZE, GRID_SIZE
                    )
                    pygame.draw.rect(surface, COLORS[game.current_piece['color']], rect)

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont('arial', size, bold=True)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Special Tetris")
    clock = pygame.time.Clock()
    game = Tetris()
    fall_time = 0
    fall_speed = 0.5

    while not game.game_over:
        screen.fill((30,30,30))
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time/1000 >= fall_speed - (game.level * 0.02):
            fall_time = 0
            if not game.move_piece(0, 1):
                game.lock_piece()  # قفل کردن قطعه در شبکه
                bomb_activated = game.handle_bomb()  # بررسی بمب
                lines_cleared = game.clear_lines()  # پاکسازی خطوط
                
                # امتیازدهی
                if lines_cleared > 0:
                    game.score += [0, 100, 300, 600, 1000][lines_cleared]
                    game.level = 1 + game.score // 1000
                
                # تولید قطعه جدید
                game.current_piece = game.next_piece
                game.next_piece = game.new_piece()
                
                # بررسی پایان بازی
                if game.check_collision(game.current_piece):
                    game.game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    while game.move_piece(0, 1):
                        pass

        draw_grid(screen, game)
        draw_text(screen, f"Score: {game.score}", 30, TOP_LEFT_X, 10)
        draw_text(screen, f"Level: {game.level}", 30, TOP_LEFT_X + 200, 10)
        pygame.display.update()

    # صفحه پایان بازی
    screen.fill((0,0,0))
    draw_text(screen, "GAME OVER!", 64, WIDTH//2 - 200, HEIGHT//2 - 50)
    draw_text(screen, f"Final Score: {game.score}", 40, WIDTH//2 - 150, HEIGHT//2 + 50)
    pygame.display.update()
    time.sleep(5)

if __name__ == "__main__":
    main()