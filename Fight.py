import pygame
import sys

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Shooting Game")

# رنگ‌ها
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# تنظیمات بازیکنان و گلوله‌ها
PLAYER_SIZE = 40
BULLET_SIZE = 8
PLAYER_SPEED = 5
BULLET_SPEED = 10
SHOOT_COOLDOWN = 30  # فریم

class Player:
    def __init__(self, x, y, color, controls):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.color = color
        self.controls = controls
        self.health = 100
        self.shoot_cooldown = 0
        self.direction = 'right'  # جهت برای شلیک

    def move(self, keys):
        # حرکت بازیکن و تغییر جهت
        if keys[self.controls['left']] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
            self.direction = 'left'
        if keys[self.controls['right']] and self.rect.x < WIDTH - PLAYER_SIZE:
            self.rect.x += PLAYER_SPEED
            self.direction = 'right'
        if keys[self.controls['up']] and self.rect.y > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[self.controls['down']] and self.rect.y < HEIGHT - PLAYER_SIZE:
            self.rect.y += PLAYER_SPEED

    def shoot(self, projectiles):
        # شلیک گلوله جدید
        if self.shoot_cooldown == 0:
            if self.direction == 'right':
                bullet = pygame.Rect(
                    self.rect.right + 1,
                    self.rect.centery - BULLET_SIZE//2,
                    BULLET_SIZE, BULLET_SIZE
                )
                velocity = BULLET_SPEED
            else:
                bullet = pygame.Rect(
                    self.rect.left - BULLET_SIZE - 1,
                    self.rect.centery - BULLET_SIZE//2,
                    BULLET_SIZE, BULLET_SIZE
                )
                velocity = -BULLET_SPEED
            
            projectiles.append({'rect': bullet, 'velocity': velocity, 'owner': self})
            self.shoot_cooldown = SHOOT_COOLDOWN

class BulletManager:
    def __init__(self):
        self.projectiles = []

    def update(self, players):
        # به روزرسانی موقعیت گلوله‌ها و تشخیص برخورد
        for proj in self.projectiles[:]:
            proj['rect'].x += proj['velocity']
            
            # حذف گلوله خارج از صفحه
            if proj['rect'].x > WIDTH or proj['rect'].x < 0:
                self.projectiles.remove(proj)
                continue
            
            # بررسی برخورد با بازیکنان
            for player in players:
                if proj['rect'].colliderect(player.rect) and player != proj['owner']:
                    player.health -= 10
                    self.projectiles.remove(proj)
                    break

# ایجاد بازیکنان
player1 = Player(100, 300, RED, {
    'left': pygame.K_a,
    'right': pygame.K_d,
    'up': pygame.K_w,
    'down': pygame.K_s,
    'shoot': pygame.K_SPACE
})

player2 = Player(600, 300, BLUE, {
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'shoot': pygame.K_RCTRL
})

bullet_manager = BulletManager()
clock = pygame.time.Clock()

# حلقه اصلی بازی
running = True
while running:
    WIN.fill(WHITE)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # حرکت بازیکنان
    player1.move(keys)
    player2.move(keys)

    # شلیک گلوله
    if keys[player1.controls['shoot']]:
        player1.shoot(bullet_manager.projectiles)
    if keys[player2.controls['shoot']]:
        player2.shoot(bullet_manager.projectiles)

    # به روزرسانی گلوله‌ها
    bullet_manager.update([player1, player2])

    # کاهش زمان تاخیر شلیک
    if player1.shoot_cooldown > 0:
        player1.shoot_cooldown -= 1
    if player2.shoot_cooldown > 0:
        player2.shoot_cooldown -= 1

    # رسم اجزا
    pygame.draw.rect(WIN, player1.color, player1.rect)
    pygame.draw.rect(WIN, player2.color, player2.rect)
    
    for proj in bullet_manager.projectiles:
        pygame.draw.rect(WIN, BLACK, proj['rect'])

    # نمایش سلامت
    pygame.draw.rect(WIN, RED, (20, 20, player1.health * 2, 20))
    pygame.draw.rect(WIN, BLUE, (WIDTH - 220, 20, player2.health * 2, 20))

    # پایان بازی
    if player1.health <= 0 or player2.health <= 0:
        font = pygame.font.SysFont(None, 72)
        text = font.render('GAME OVER!', True, BLACK)
        WIN.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 40))
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()