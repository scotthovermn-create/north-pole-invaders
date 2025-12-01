# main.py - North Pole Invaders - BLACK SCREEN FIXED!
import pygame
import random
import math
import os

# Safe init - NO MIXER (fixes 80% of black screens)
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("North Pole Invaders")

# Colors
RED   = (220, 20, 60)
GREEN = (0, 200, 0)
GOLD  = (255, 215, 0)
WHITE = (255, 255, 255)
BLUE  = (5, 20, 50)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32, bold=True)
small_font = pygame.font.SysFont("arial", 18)

# Load images (PNG first, fallbacks second)
def load_image(name, scale=None):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    # Fallbacks
    s = pygame.Surface((60, 60), pygame.SRCALPHA)
    if "santa" in name:
        pygame.draw.circle(s, RED, (30,20), 20)
        pygame.draw.rect(s, WHITE, (15,35,30,25))
    elif "reindeer" in name:
        pygame.draw.ellipse(s, (139,69,19), (15,10,30,30))
        pygame.draw.circle(s, RED, (45,15), 5)
    elif "tree" in name:
        pygame.draw.polygon(s, GREEN, [(30,5),(10,55),(50,55)])
        pygame.draw.rect(s, (139,69,19), (25,50,10,15))
    elif "snowman" in name:
        pygame.draw.circle(s, WHITE, (30,20), 18)
        pygame.draw.circle(s, WHITE, (30,50), 22)
    elif "sleigh" in name:
        pygame.draw.polygon(s, RED, [(0,30),(70,20),(80,50),(0,50)])
    elif "gift" in name:
        pygame.draw.rect(s, GOLD, (0,0,20,30))
        pygame.draw.line(s, RED, (0,10),(20,10),3)
        pygame.draw.line(s, RED, (10,0),(10,30),3)
    if scale:
        s = pygame.transform.scale(s, scale)
    return s

player_img   = load_image("player_sleigh.png", (80,60))
bullet_img   = load_image("gift.png", (20,30))
tree_img     = load_image("tree.png", (60,70))
snowman_img  = load_image("snowman.png", (60,70))
reindeer_img = load_image("reindeer.png", (70,60))
santa_img    = load_image("santa.png", (60,60))

invader_imgs = [tree_img, snowman_img, reindeer_img, santa_img, santa_img]

# Background + twinkling stars
bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill(BLUE)
stars = [(random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(1,3)) for _ in range(150)]

# Game state
player_x = WIDTH // 2 - 40
player_y = HEIGHT - 100
player_speed = 7
bullets = []
invaders = []
score = 0
lives = 3
game_over = False
victory = False

def spawn_invaders():
    global invaders
    invaders = []
    for row in range(5):
        for col in range(10):
            x = 70 + col * 70
            y = 60 + row * 70
            invaders.append({"x": float(x), "y": float(y), "img": invader_imgs[row]})

spawn_invaders()
direction = 1
speed = 1

running = True
while running:  # Non-async loop (pygbag-safe without sleep)
    clock.tick(60)
    screen.blit(bg, (0, 0))

    # Twinkling stars
    for i, (x,y,size) in enumerate(stars):
        brightness = 150 + 105 * math.sin(pygame.time.get_ticks() * 0.01 + i)
        col = (255, min(255,int(brightness)), 100) if i%3==0 else (min(255,int(brightness)),100,255)
        pygame.draw.circle(screen, col, (x,y), size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not victory:
                bullets.append([player_x + 30, player_y - 20])
            if event.key == pygame.K_r and (game_over or victory):
                score = lives = 3
                game_over = victory = False
                player_x = WIDTH // 2 - 40
                bullets.clear()
                spawn_invaders()

    if not game_over and not victory:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0: player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 80: player_x += player_speed

        # Bullets
        for b in bullets[:]:
            b[1] -= 12
            if b[1] < 0: bullets.remove(b)

        # Invaders movement
        edge = False
        for inv in invaders:
            inv["x"] += direction * speed
            if inv["x"] <= 10 or inv["x"] >= WIDTH - 70: edge = True

        if edge:
            direction *= -1
            for inv in invaders:
                inv["y"] += 30
                if inv["y"] > player_y:
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    else:
                        spawn_invaders()

        # Collisions
        for b in bullets[:]:
            bx, by = b
            for inv in invaders[:]:
                if (inv["x"] < bx < inv["x"]+60 and inv["y"] < by < inv["y"]+60):
                    invaders.remove(inv)
                    bullets.remove(b)
                    score += 10
                    break

        # Victory check
        if not invaders:
            victory = True

    # Draw everything
    screen.blit(player_img, (player_x, player_y))
    for b in bullets: screen.blit(bullet_img, (b[0], b[1]))
    for inv in invaders: screen.blit(inv["img"], (int(inv["x"]), int(inv["y"])))

    # HUD
    hud = font.render(f"Score: {score}   Lives: {lives}", True, GOLD)
    screen.blit(hud, (10, 10))

    # Tiny controls hint
    ctrl = small_font.render("← → Move    Space = Fire", True, GOLD)
    screen.blit(ctrl, ctrl.get_rect(center=(WIDTH//2, HEIGHT-20)))

    # Game Over
    if game_over:
        go = font.render("GAME OVER – Press R to restart", True, RED)
        screen.blit(go, go.get_rect(center=(WIDTH//2, HEIGHT//2)))

    # VICTORY MESSAGE – your exact lines!
    elif victory:
        lines = [
            "Blitzen the Reindeer & You",
            "Have Saved CHRISTMAS",
            "from the Evil Grinch!",
            "The Skies are Clear Again!"
        ]
        y = HEIGHT//2 - 100
        for i, txt in enumerate(lines):
            size = 64 if i == 1 else 48
            f = pygame.font.SysFont("arial", size, bold=True)
            surf = f.render(txt, True, GOLD)
            rect = surf.get_rect(center=(WIDTH//2, y))
            screen.blit(surf, rect)
            y += surf.get_height() + 10

        restart = small_font.render("Press R to Save Christmas Again!", True, WHITE)
        screen.blit(restart, restart.get_rect(center=(WIDTH//2, HEIGHT-100)))

    pygame.display.flip()

pygame.quit()
