# main.py - North Pole Invaders - SMOOTH & PERFECT!
import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("North Pole Invaders")

# Colors
GREEN = (0, 180, 0)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
NIGHT_BLUE = (5, 20, 50)

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 36)
big_font = pygame.font.SysFont("comicsansms", 72, bold=True)

# ALL GLOBALS FIRST!
invaders = []
bullets = []
score = 0
lives = 3
game_over = False
victory = False
invader_direction = 1
player_x = float(WIDTH // 2 - 40)
player_y = HEIGHT - 100
player_speed = 8.0
bullet_speed = 12
invader_speed = 1.5  # SMOOTH FLOAT NOW!
invader_drop = 25

def load_image(name, scale=None):
    path = os.path.join("assets", name)
    if not os.path.exists(path):
        img = pygame.Surface((60, 60), pygame.SRCALPHA)
        if "santa" in name:
            pygame.draw.circle(img, RED, (30, 20), 20); pygame.draw.rect(img, WHITE, (20, 35, 20, 25))
        elif "reindeer" in name:
            pygame.draw.polygon(img, (139, 69, 19), [(30,10),(20,30),(40,30)]); pygame.draw.circle(img, (139, 69, 19), (30, 40), 20)
        elif "tree" in name:
            pygame.draw.polygon(img, GREEN, [(30,10),(10,50),(50,50)]); pygame.draw.rect(img, (139, 69, 19), (25, 50, 10, 20))
        elif "snowman" in name:
            pygame.draw.circle(img, WHITE, (30, 20), 15); pygame.draw.circle(img, WHITE, (30, 45), 20)
        elif "sleigh" in name:
            pygame.draw.polygon(img, RED, [(10,40),(50,30),(70,50),(10,50)])
        elif "gift" in name:
            pygame.draw.rect(img, RED, (10, 10, 40, 40)); pygame.draw.rect(img, GOLD, (25, 5, 10, 50))
        return img
    img = pygame.image.load(path).convert_alpha()
    if scale: img = pygame.transform.scale(img, scale)
    return img

# Load assets
santa_img = load_image("santa.png", (60, 60))
reindeer_img = load_image("reindeer.png", (70, 60))
tree_img = load_image("tree.png", (60, 70))
snowman_img = load_image("snowman.png", (60, 70))
player_img = load_image("player_sleigh.png", (80, 60))
bullet_img = load_image("gift.png", (20, 30))
invader_images = [tree_img, snowman_img, reindeer_img, santa_img, santa_img]

# Background & stars
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(NIGHT_BLUE)
for _ in range(200): pygame.draw.circle(background, WHITE, (random.randint(0,WIDTH), random.randint(0,HEIGHT)), random.randint(1,3))
stars = [(random.randint(0,WIDTH), random.randint(0,100), random.randint(1,3)) for _ in range(80)]

def reset_invaders():
    global invaders, invader_direction
    invaders.clear()
    for row in range(5):
        for col in range(10):
            img = invader_images[row]
            x = 30.0 + col * 65.0
            y = 80.0 + row * 75.0
            rect = pygame.Rect(x, y, img.get_width(), img.get_height())
            invaders.append({"x": x, "y": y, "rect": rect, "img": img, "type": row})
    invader_direction = 1

def reset_game():
    global score, lives, game_over, victory, bullets, player_x, invaders, invader_direction
    score = 0; lives = 3; game_over = False; victory = False
    bullets.clear(); player_x = float(WIDTH//2 - 40)
    reset_invaders()

reset_game()

try:
    shoot_sound = pygame.mixer.Sound(os.path.join("assets", "twinkling.wav"))
    shoot_sound.set_volume(0.3)
except: shoot_sound = None

running = True
while running:
    clock.tick(60)
    screen.blit(background, (0,0))

    # Twinkling stars
    for i, (x,y,size) in enumerate(stars):
        brightness = 150 + 105 * math.sin(pygame.time.get_ticks() * 0.01 + i)
        color = (255, min(255,int(brightness)), 100) if i%3==0 else (min(255,int(brightness)),100,255)
        pygame.draw.circle(screen, color, (x,y), size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not
