import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Game")

# Colors
WHITE = (255, 255, 255)
BALL_COLOR = (255, 100, 100)
PADDLE_COLOR = (100, 200, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)

def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(None, size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(rendered, rect)

def game_over_screen(score):
    screen.fill(WHITE)
    draw_text("GAME OVER", 48, BLACK, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text(f"Final Score: {score}", 36, BLACK, WIDTH // 2, HEIGHT // 2)
    draw_text("Press R to Restart or Q to Quit", 24, BLACK, WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Restart game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def run_game():
    # Ball setup
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_radius = 15
    ball_vel = [random.choice([-4, 4]), -4]

    # Paddle setup
    paddle_width = 100
    paddle_height = 15
    paddle_pos = [WIDTH // 2 - paddle_width // 2, HEIGHT - 50]
    paddle_speed = 7

    # Score
    score = 0

    # Clock
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
            paddle_pos[0] -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_pos[0] < WIDTH - paddle_width:
            paddle_pos[0] += paddle_speed

        # Ball movement
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        # Bounce off walls
        if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
            ball_vel[0] *= -1
        if ball_pos[1] <= ball_radius:
            ball_vel[1] *= -1

        # Bounce off paddle
        if (
            paddle_pos[1] < ball_pos[1] + ball_radius < paddle_pos[1] + paddle_height and
            paddle_pos[0] < ball_pos[0] < paddle_pos[0] + paddle_width
        ):
            ball_vel[1] *= -1
            score += 1

        # Game over
        if ball_pos[1] > HEIGHT:
            game_over_screen(score)
            return  # Exit this run, go back to main loop

        # Draw everything
        pygame.draw.circle(screen, BALL_COLOR, ball_pos, ball_radius)
        pygame.draw.rect(screen, PADDLE_COLOR, (*paddle_pos, paddle_width, paddle_height))

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

# === Main loop ===
while True:
    run_game()
