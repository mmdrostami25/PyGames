import pygame
import random

# Initialize pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # I - Cyan
    (0, 0, 255),    # J - Blue
    (255, 165, 0),  # L - Orange
    (255, 255, 0),  # O - Yellow
    (0, 255, 0),    # S - Green
    (128, 0, 128),  # T - Purple
    (255, 0, 0)     # Z - Red
]

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
GAME_AREA_LEFT = CELL_SIZE

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    
    [[1, 0, 0],
     [1, 1, 1]],     # J
    
    [[0, 0, 1],
     [1, 1, 1]],     # L
    
    [[1, 1],
     [1, 1]],        # O
    
    [[0, 1, 1],
     [1, 1, 0]],     # S
    
    [[0, 1, 0],
     [1, 1, 1]],     # T
    
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

class Tetrimino:
    def __init__(self, x, y, shape_idx):
        self.x = x
        self.y = y
        self.shape_idx = shape_idx
        self.shape = SHAPES[shape_idx]
        self.color = COLORS[shape_idx]
        self.rotation = 0
    
    def rotate(self):
        # Transpose and reverse to rotate 90 degrees clockwise
        rows = len(self.shape)
        cols = len(self.shape[0])
        rotated = [[0 for _ in range(rows)] for _ in range(cols)]
        
        for r in range(rows):
            for c in range(cols):
                rotated[c][rows-1-r] = self.shape[r][c]
        
        return rotated
    
    def get_rotated_shape(self):
        return self.rotate()
    
    def draw(self, x_offset=0, y_offset=0, small=False):
        size = CELL_SIZE // 2 if small else CELL_SIZE
        shape = self.shape if self.rotation == 0 else self.get_rotated_shape()
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (self.x + x + x_offset) * size,
                        (self.y + y + y_offset) * size,
                        size - 1, size - 1
                    )
                    pygame.draw.rect(screen, self.color, rect)

class TetrisGame:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 0.5  # seconds
        self.fall_time = 0
    
    def new_piece(self):
        shape_idx = random.randint(0, len(SHAPES) - 1)
        return Tetrimino(GRID_WIDTH // 2 - len(SHAPES[shape_idx][0]) // 2, 0, shape_idx)
    
    def valid_move(self, piece, x_offset=0, y_offset=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + x_offset
                    new_y = piece.y + y + y_offset
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or 
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True
    
    def merge_piece(self):
        shape = self.current_piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell and self.current_piece.y + y >= 0:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
    
    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = len(self.grid) - len(new_grid)
        
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += [100, 300, 500, 800][lines_cleared - 1] * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)
            
            for _ in range(lines_cleared):
                new_grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            
            self.grid = new_grid
    
    def update(self, delta_time):
        if self.game_over:
            return
        
        self.fall_time += delta_time
        
        # Move piece down automatically
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if self.valid_move(self.current_piece, 0, 1):
                self.current_piece.y += 1
            else:
                self.merge_piece()
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()
                
                if not self.valid_move(self.current_piece):
                    self.game_over = True
    
    def draw(self):
        # Draw game area border
        pygame.draw.rect(
            screen, WHITE, 
            (GAME_AREA_LEFT - 2, 0, GRID_WIDTH * CELL_SIZE + 4, GRID_HEIGHT * CELL_SIZE + 4), 2
        )
        
        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(
                        screen, self.grid[y][x],
                        (GAME_AREA_LEFT + x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1)
                    )
        
        # Draw current piece
        if not self.game_over:
            self.current_piece.draw(GAME_AREA_LEFT / CELL_SIZE)
        
        # Draw next piece preview
        font = pygame.font.SysFont(None, 30)
        next_text = font.render("Next:", True, WHITE)
        screen.blit(next_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10, 10))
        
        self.next_piece.draw(
            (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 30) / (CELL_SIZE // 2),
            30 / (CELL_SIZE // 2),
            True
        )
        
        # Draw score and level
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        lines_text = font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        screen.blit(score_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10, 100))
        screen.blit(level_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10, 130))
        screen.blit(lines_text, (GAME_AREA_LEFT + GRID_WIDTH * CELL_SIZE + 10, 160))
        
        # Draw game over
        if self.game_over:
            font = pygame.font.SysFont(None, 48)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(
                game_over_text,
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2)
            )
            
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(
                restart_text,
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                 SCREEN_HEIGHT // 2 + 50)
            )

def main():
    game = TetrisGame()
    running = True
    
    while running:
        delta_time = clock.tick(60) / 1000.0  # Convert to seconds
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if not game.game_over:
                    if event.key == pygame.K_LEFT and game.valid_move(game.current_piece, -1, 0):
                        game.current_piece.x -= 1
                    elif event.key == pygame.K_RIGHT and game.valid_move(game.current_piece, 1, 0):
                        game.current_piece.x += 1
                    elif event.key == pygame.K_DOWN and game.valid_move(game.current_piece, 0, 1):
                        game.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        rotated = game.current_piece.get_rotated_shape()
                        if game.valid_move(game.current_piece, 0, 0, rotated):
                            game.current_piece.shape = rotated
                    elif event.key == pygame.K_SPACE:  # Hard drop
                        while game.valid_move(game.current_piece, 0, 1):
                            game.current_piece.y += 1
                        game.merge_piece()
                        game.clear_lines()
                        game.current_piece = game.next_piece
                        game.next_piece = game.new_piece()
                        
                        if not game.valid_move(game.current_piece):
                            game.game_over = True
                else:
                    if event.key == pygame.K_r:  # Restart game
                        game = TetrisGame()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and not game.game_over:
            game.fall_speed = 0.05
        
        game.update(delta_time)
        game.draw()
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()