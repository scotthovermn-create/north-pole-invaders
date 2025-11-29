# main.py - North Pole Invaders - Merry Christmas Edition! (Fixed formation)
import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("North Pole Invaders")

# Colors (Christmas palette)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
NIGHT_BLUE = (5, 20, 50)

# Clock & Font
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 36)
big_font = pygame.font.SysFont("comicsansms", 72, bold=True)

# Load assets (with fallbacks if missing)
def load_image(name, scale=None):
    path = os.path.join("assets", name)
    if not os.path.exists(path):
        # Return a colored surface if image missing
        img = pygame.Surface((60, 60), pygame.SRCALPHA)
        if "santa" in name:
            pygame.draw.circle(img, RED, (30, 20), 20)
            pygame.draw.rect(img, WHITE, (20, 35, 20, 25))
        elif "reindeer" in name:
            pygame.draw.polygon(img, (139, 69, 19), [(30,10),(20,30),(40,30)])
            pygame.draw.circle(img, (139, 69, 19), (30, 40), 20)
        elif "tree" in name:
            pygame.draw.polygon(img, GREEN, [(30,10),(10,50),(50,50)])
            pygame.draw.rect(img, (139, 69, 19), (25, 50, 10, 20))
        elif "snowman" in name:
            pygame.draw.circle(img, WHITE, (30, 20), 15)
            pygame.draw.circle(img, WHITE, (30, 45), 20)
        elif "sleigh" in name:
            pygame.draw.polygon(img, RED, [(10,40),(50,30),(70,50),(10,50)])
        elif "gift" in name:
            pygame.draw.rect(img, RED, (10, 10, 40, 40))
            pygame.draw.rect(img, GOLD, (25, 5, 10, 50))
        return img
    img = pygame.image.load(path).convert_alpha()
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

# Load images
santa_img = load_image("santa.png", (60, 60))
reindeer_img = load_image("reindeer.png", (70, 60))
tree_img = load_image("tree.png", (60, 70))
snowman_img = load_image("snowman.png", (60, 70))
player_img = load_image("player_sleigh.png", (80, 60))
bullet_img = load_image("gift.png", (20, 30))

invader_images = [tree_img, snowman_img, reindeer_img, santa_img, santa_img]

# Background (night sky with static snowflakes)
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(NIGHT_BLUE)
for _ in range(200):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    pygame.draw.circle(background, WHITE, (x, y), random.randint(1, 3))

# Twinkling stars/lights
stars = [(random.randint(0, WIDTH), random.randint(0, 100), random.randint(1, 3)) for _ in range(80)]

def reset_invaders():
    global invaders, invader_direction
    invaders.clear()
    invader_cols = 10
    invader_offset_x = 30
    invader_spacing_x = 65
    invader_offset_y = 80
    invader_spacing_y = 75
    for row in range(5):
        for col in range(invader_cols):
            img = invader_images[row]
            x = invader_offset_x + col * invader_spacing_x
            y = invader_offset_y + row * invader_spacing_y
            rect = img.get_rect(topleft=(x, y))
            invaders.append({"rect": rect, "img": img, "type": row})
    invader_direction = 1

# Player
player_x = WIDTH // 2 - 40
player_y = HEIGHT - 100
player_speed = 8

# Game state
def reset_game():
    global score, lives, game_over, victory, bullets, player_x, invaders, invader_direction
    score = 0
    lives = 3
    game_over = False
    victory = False
    bullets.clear()
    player_x = WIDTH // 2 - 40
    reset_invaders()

reset_game()  # Initial setup

# Movement vars
bullets = []
bullet_speed = 12
invader_speed = 0.8
invader_drop = 25
invader_direction = 1

# Sound (optional)
try:
    shoot_sound = pygame.mixer.Sound(os.path.join("assets", "twinkling.wav"))
    shoot_sound.set_volume(0.3)
except:
    shoot_sound = None

# Main game loop
running = True
while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    # Twinkling Christmas lights
    for i, (x, y, size) in enumerate(stars):
        brightness = 150 + 105 * math.sin(pygame.time.get_ticks() * 0.01 + i)
        color = (255, min(255, int(brightness)), 100) if i % 3 == 0 else (min(255, int(brightness)), 100, 255)
        pygame.draw.circle(screen, color, (x, y), size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not victory:
                bullets.append(pygame.Rect(player_x + 35, player_y, 20, 30))
                if shoot_sound:
                    shoot_sound.play()
            if event.key == pygame.K_r and (game_over or victory):
                reset_game()

    if not game_over and not victory:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 80:
            player_x += player_speed

        # Move bullets up
        for b in bullets[:]:
            b.y -= bullet_speed
            if b.y < 0:
                bullets.remove(b)

        # Move invaders
        move_down = False
        for inv in invaders:
            inv["rect"].x += invader_direction * invader_speed
            if inv["rect"].right >= WIDTH or inv["rect"].left <= 0:
                move_down = True

        if move_down:
            invader_direction *= -1
            lost_life = False
            for inv in invaders:
                inv["rect"].y += invader_drop
                if inv["rect"].top > player_y:
                    lost_life = True
            if lost_life:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    reset_invaders()  # Respawn wave

        # Collision: bullets hit invaders
        for b in bullets[:]:
            hit = False
            for inv in invaders[:]:
                if b.colliderect(inv["rect"]):
                    invaders.remove(inv)
                    bullets.remove(b)
                    score += 10 if inv["type"] < 4 else 50
                    hit = True
                    break
            if hit:
                continue

        # Check victory
        if len(invaders) == 0:
            victory = True

    # Draw game objects
    screen.blit(player_img, (player_x, player_y))
    for b in bullets:
        screen.blit(bullet_img, (b.x, b.y))
    for inv in invaders:
        screen.blit(inv["img"], inv["rect"])

    # UI
    score_text = font.render(f"Score: {score}", True, GOLD)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

    # Merry Christmas!
    merry_text = big_font.render("Merry Christmas!", True, GOLD)
    text_rect = merry_text.get_rect(center=(WIDTH//2, HEIGHT - 40))
    pygame.draw.rect(screen, DARK_GREEN, (text_rect.x - 20, text_rect.y - 10, text_rect.width + 40, text_rect.height + 20))
    pygame.draw.rect(screen, WHITE, (text_rect.x - 15, text_rect.y - 5, text_rect.width + 30, text_rect.height + 10), 2)
    screen.blit(merry_text, text_rect)

    # Game Over / Victory screens
    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))
    elif victory:
        win_text = big_font.render("YOU SAVED CHRISTMAS!", True, GOLD)
        restart_text = font.render("Press R for More!", True, WHITE)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30)))
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30)))

    pygame.display.flip()

pygame.quit()
