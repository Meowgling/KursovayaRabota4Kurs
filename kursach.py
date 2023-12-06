import pygame
import random

# инициализация Pygame
pygame.init()

# установка размеров экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Арканоид')

# определение цветов
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# параметры платформы (игрока) и шарика
platform_width = 100
platform_height = 10
platform_x = SCREEN_WIDTH // 2 - platform_width // 2
platform_y = SCREEN_HEIGHT - 30
platform_speed = 2.5

ball_radius = 10
ball_x = platform_x + platform_width // 2
ball_y = platform_y - ball_radius
ball_speed_x = random.choice([-0.25, 0.25]) * random.uniform(1, 3)
ball_speed_y = -0.25

# параметры блоков
block_width = 70
block_height = 20
blocks = []
for row in range(3):
    for column in range(4):
        block = pygame.Rect(175 + column * (block_width + 10), 70 + row * (block_height + 5), block_width, block_height)
        blocks.append(block)

# начальные параметры игры
lives = 3
score = 0
game_over = False

# функция отрисовки объектов на экране
def draw_objects():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (platform_x, platform_y, platform_width, platform_height))
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    for block in blocks:
        pygame.draw.rect(screen, RED, block)

    font = pygame.font.Font(None, 36)
    score_text = font.render('Очки: ' + str(score), True, RED)
    screen.blit(score_text, (20, 20))

    lives_text = font.render('Жизни: ' + str(lives), True, RED)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 20))

    pygame.display.flip()

# основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        draw_objects()

        # движение платформы
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            platform_x -= platform_speed
        if keys[pygame.K_RIGHT]:
            platform_x += platform_speed

        # ограничение движения платформы
        if platform_x < 0:
            platform_x = 0
        if platform_x + platform_width > SCREEN_WIDTH:
            platform_x = SCREEN_WIDTH - platform_width

        # движение шарика
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # отскок от стен
        if ball_x <= 0 or ball_x >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # обработка столкновения шарика с платформой
        if ball_y >= platform_y - ball_radius and platform_x < ball_x < platform_x + platform_width:
            ball_speed_y = -ball_speed_y

        # обработка столкновения шарика с блоками
        for block in blocks:
            if block.colliderect((ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
                ball_speed_y = -ball_speed_y
                blocks.remove(block)
                score += 10

        # обработка потери жизни
        if ball_y > SCREEN_HEIGHT:
            lives -= 1
            if lives == 0:
                game_over = True

        # обработка победы
        if not blocks:
            game_over = True

        # перезапуск шарика
        if game_over:
            pygame.time.wait(1000)
            ball_x = platform_x + platform_width // 2
            ball_y = platform_y - ball_radius
            ball_speed_x = random.choice([-1, 1]) * random.uniform(1, 3)
            ball_speed_y = -3
            if lives == 0:
                text = "Поражение"
            else:
                text = "Победа"
            font = pygame.font.Font(None, 36)
            text = font.render(text, True, RED)
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break
    pygame.display.update()