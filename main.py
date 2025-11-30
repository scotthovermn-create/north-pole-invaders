# main.py - North Pole Invaders - SIMPLE & BULLETPROOF
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("North Pole Invaders")

# Colors
RED = (220, 20, 60)
GREEN = (0, 200, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
BLUE = (5, 20, 50)

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32, bold=True)

# Game vars
player_x = WIDTH // 2 - 40
player_y = HEIGHT - 100
player_speed = 7

bullets = []
invaders = []
score = 0
lives = 3
game_over = False

# Simple sprites WITH PNG LOADING (tries assets first!)
def load_image(name, scale=None):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    # Fallback shapes if PNG missing
    img = pygame.Surface((60, 60), pygame.SRCALPHA)
    if "santa" in name:
        pygame.draw.circle(img, RED, (30,20), 20)
        pygame.draw.rect(img, WHITE, (15,35,30,25))
    elif "reindeer" in name:
        pygame.draw.ellipse(img, (139,69,19), (15,10,30,30))
        pygame.draw.circle(img, RED, (30,5), 3)  # Red nose
    elif "tree" in name:
        pygame.draw.polygon(img, GREEN, [(30,5),(10,55),(50,55)])
        pygame.draw.rect(img, (139,69,19), (25,50,10,15))
    elif "snowman" in name:
        pygame.draw.circle(img, WHITE, (30,20), 18)
        pygame.draw.circle(img, WHITE, (30,50), 22)
    elif "sleigh" in name:
        pygame.draw.polygon(img, RED, [(0,30),(70,20),(80,50),(0,50)])
    elif "gift" in name:
        pygame.draw.rect(img, GOLD, (0,0,20,30))
        pygame.draw.line(img, RED, (0,10), (20,10), 2)
        pygame.draw.line(img, RED, (10,0), (10,30), 2)
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

# Load PNGs (or fallbacks)
player_img = load_image("player_sleigh.png", (80, 60))
bullet_img = load_image("gift.png", (20, 30))
tree_img = load_image("tree.png", (60, 70))
snowman_img = load_image("snowman.png", (60, 70))
reindeer_img = load_image("reindeer.png", (70, 60))
santa_img = load_image("santa.png", (60, 60))

invader_imgs = [tree_img, snowman_img, reindeer_img, santa_img, santa_img]

# Background with twinkles
bg = pygame.Surface((WIDTH, HEIGHT))
bg.fill(BLUE)
stars = [(random.randint(0,WIDTH), random.randint(0,HEIGHT), random.randint(1,3)) for _ in range(150)]

def spawn_invaders():
    global invaders
    invaders = []
    for row in range(5):
        for col in range(10):
            x = 70 + col * 70
            y = 60 + row * 70
            invaders.append({"x": float(x), "y": float(y), "img": invader_imgs[row], "type": row})

spawn_invaders()
direction = 1
speed = 1

running = True
while running:
    clock.tick(60)
    screen.blit(bg, (0, 0))

    # Twinkling stars
    for i, (x, y, size) in enumerate(stars):
        brightness = 150 + 105 * math.sin(pygame.time.get_ticks() * 0.01 + i)
        color = (255, min(255, int(brightness)), 100) if i % 3 == 0 else (min(255, int(brightness)), 100, 255)
        pygame.draw.circle(screen, color, (x, y), size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x + 30, player_y - 20])
            if event.key == pygame.K_r and game_over:
                score = 0
                lives = 3
                game_over = False
                player_x = WIDTH // 2 - 40
                spawn_invaders()

    if not game_over:
        # Player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0: player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 80: player_x += player_speed

        # Bullets
        for b in bullets[:]:
            b[1] -= 10
            if b[1] < 0: bullets.remove(b)

        # Invaders
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

        if not invaders:
            spawn_invaders()

    # Draw
    screen.blit(player_img, (player_x, player_y))
    for b in bullets: screen.blit(bullet_img, (b[0], b[1]))
    for inv in invaders: screen.blit(inv["img"], (int(inv["x"]), int(inv["y"])))

    # HUD
    hud = font.render(f"Score: {score}  Lives: {lives}", True, GOLD)
    screen.blit(hud, (10, 10))

    if game_over:
        go = font.render("GAME OVER - Press R to restart", True, RED)
        screen.blit(go, (WIDTH//2 - go.get_width()//2, HEIGHT//2))

        
    # Tiny "Controls" text at bottom center (festive gold tint)
    small_font = pygame.font.SysFont("arial", 18, bold=False)  # Very small
    controls_surf = small_font.render("← → Move    Space = Fire", True, GOLD)  # Gold for Christmas vibe
    
    controls_rect = controls_surf.get_rect(center=(WIDTH // 2, HEIGHT - 20))  # 20px from bottom
    screen.blit(controls_surf, controls_rect)
    
    pygame.display.flip()  
  

pygame.quit()
