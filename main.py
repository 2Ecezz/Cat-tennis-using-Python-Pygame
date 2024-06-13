import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED_X = 10
BALL_SPEED_Y = 10
PADDLE_SPEED = 8
PLAYER_PADDLE_SCALE = (100, 100)
BOT_PADDLE_SCALE = (80, 80)
BALL_SCALE = (50, 50)
PLAYER_MAX_SCALE = 5  # Increase the max scale for player paddle
PLAYER_MIN_SCALE = 2  # Minimum scale for player paddle
BOT_MAX_SCALE = 1.5
BOT_MIN_SCALE = 0.5
BALL_MAX_SCALE = 3
BALL_MIN_SCALE = 0.5

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("3D Cat Tennis Game")

pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play(-1)  # Play the music indefinitely

try:
    # Load the background image
    background = pygame.image.load('background.png').convert()

    # Scale the background image to fit the screen size
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    player_paddle_img = pygame.image.load('player_paddle.png').convert_alpha()
    bot_paddle_img = pygame.image.load('bot_paddle.png').convert_alpha()
    ball_img = pygame.image.load('ball.png').convert_alpha()
    cat_img = pygame.image.load('cat.gif').convert_alpha()  # Load the cat image

    player_paddle_img = pygame.transform.scale(player_paddle_img, PLAYER_PADDLE_SCALE)
    bot_paddle_img = pygame.transform.scale(bot_paddle_img, BOT_PADDLE_SCALE)
    ball_img = pygame.transform.scale(ball_img, BALL_SCALE)
    cat_img = pygame.transform.scale(cat_img, (150, 150))  # Scale the cat image

except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    sys.exit()

# Define the paddle and ball positions relative to the screen
player_paddle_rect = player_paddle_img.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
bot_paddle_rect = bot_paddle_img.get_rect(midtop=(SCREEN_WIDTH // 2, 50))
ball_rect = ball_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
cat_rect = cat_img.get_rect(center=bot_paddle_rect.center)

# Ball velocity
ball_velocity = [BALL_SPEED_X, BALL_SPEED_Y]

# Scores
player_score = 0
bot_score = 0

# Functions
def move_player_paddle():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_paddle_rect.centerx = mouse_x
    player_paddle_rect.centery = mouse_y
    player_paddle_rect.left = max(0, player_paddle_rect.left)
    player_paddle_rect.right = min(SCREEN_WIDTH, player_paddle_rect.right)
    player_paddle_rect.top = max(SCREEN_HEIGHT // 2, player_paddle_rect.top)
    player_paddle_rect.bottom = min(SCREEN_HEIGHT, player_paddle_rect.bottom)

def move_bot_paddle():
    if bot_paddle_rect.centerx < ball_rect.centerx:
        bot_paddle_rect.x += PADDLE_SPEED
    elif bot_paddle_rect.centerx > ball_rect.centerx:
        bot_paddle_rect.x -= PADDLE_SPEED
    bot_paddle_rect.left = max(0, bot_paddle_rect.left)
    bot_paddle_rect.right = min(SCREEN_WIDTH, bot_paddle_rect.right)

def move_ball():
    ball_rect.x += ball_velocity[0]
    ball_rect.y += ball_velocity[1]

def check_collision():
    global ball_velocity
    if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
        ball_velocity[0] = -ball_velocity[0]
    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        ball_velocity[1] = -ball_velocity[1]
    if ball_rect.colliderect(player_paddle_rect):
        ball_velocity[1] = -abs(ball_velocity[1])  # Ensure ball moves up
    if ball_rect.colliderect(bot_paddle_rect):
        ball_velocity[1] = abs(ball_velocity[1])  # Ensure ball moves down

def reset_ball():
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    return [BALL_SPEED_X, BALL_SPEED_Y]

def update_scores():
    global player_score, bot_score, ball_velocity
    if ball_rect.top <= 0:
        player_score += 1
        ball_velocity = reset_ball()
    if ball_rect.bottom >= SCREEN_HEIGHT:
        bot_score += 1
        ball_velocity = reset_ball()

def display_score():
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Player: {player_score}", True, BLACK)
    bot_text = font.render(f"Bot: {bot_score}", True, BLACK)
    screen.blit(player_text, (20, SCREEN_HEIGHT - 40))
    screen.blit(bot_text, (SCREEN_WIDTH - 150, 10))

def scale_and_blit(img, rect, min_scale, max_scale):
    # Scale factor calculation
    scale_factor = min_scale + (max_scale - min_scale) * (1 - rect.centery / SCREEN_HEIGHT)
    scaled_img = pygame.transform.scale(img, (int(rect.width * scale_factor), int(rect.height * scale_factor)))
    new_rect = scaled_img.get_rect(center=rect.center)
    screen.blit(scaled_img, new_rect)

# Main game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_player_paddle()
    move_bot_paddle()
    move_ball()
    check_collision()
    update_scores()

    # Update cat position
    cat_rect.center = bot_paddle_rect.center

    # Clear the screen
    screen.blit(background, (0, 0))

    # Draw the cat image at the bot paddle position
    screen.blit(cat_img, cat_rect)

    # Draw paddles and ball relative to the background image
    scale_and_blit(player_paddle_img, player_paddle_rect, PLAYER_MIN_SCALE, PLAYER_MAX_SCALE)
    scale_and_blit(bot_paddle_img, bot_paddle_rect, BOT_MIN_SCALE, BOT_MAX_SCALE)
    scale_and_blit(ball_img, ball_rect, BALL_MIN_SCALE, BALL_MAX_SCALE)

    # Display score
    display_score()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
