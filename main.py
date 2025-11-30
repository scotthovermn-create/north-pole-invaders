# main.py - North Pole Invaders - PERFECTLY PLAYABLE!
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

# ALL GLOBALS FIRST! (CRASH FIX)
invaders = []
bullets = []
score = 0
lives = 3
game_over = False
victory = False
invader_direction = 1
player_x = WIDTH // 2 - 40
player_y = HEIGHT - 100
player_speed = 8
bullet_speed = 10
invader_speed = 1  # SLOW WAS 2.5 FAST NOW!
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
            x = 30 + col * 65
            y = 80 + row * 75
            rect = img.get_rect(topleft=(x, y))
            invaders.append({"rect": rect, "img": img, "type": row})
    invader_direction = 1

def reset_game():
    global score, lives, game_over, victory, bullets, player_x, invaders, invader_direction
    score = 0; lives = 3; game_over = False; victory = False
    bullets.clear(); player_x = WIDTH//2 - 40
    reset_invaders()

reset_game()  # NOW SAFE!

try:
    shoot_sound = pygame.mixer.Sound(os.path.join("assets", "twinkling.wav"))
    shoot_sound.set_volume(0.3)
except: shoot_sound = None

running = True
while running:
    clock.tick(60)
    screen.blit(background, (0,0))

    # Twinkling
    for i, (x,y,size) in enumerate(stars):
        brightness = 150 + 105 * math.sin(pygame.time.get_ticks() * 0.01 + i)
        color = (255, min(255,int(brightness)), 100) if i%3==0 else (min(255,int(brightness)),100,255)
        pygame.draw.circle(screen, color, (x,y), size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not victory:
                bullets.append(pygame.Rect(player_x + 35, player_y, 20, 30))
                if shoot_sound: shoot_sound.play()
            if event.key == pygame.K_r and (game_over or victory): reset_game()

    if not game_over and not victory:
        # Player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0: player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 80: player_x += player_speed

        # Bullets
        for b in bullets[:]:
            b.y -= bullet_speed
            if b.y < 0: bullets.remove(b)

        # INVADERS MARCH!
        move_down = False
        for inv in invaders:
            inv["rect"].x += invader_direction * invader_speed
            if inv["rect"].right >= WIDTH or inv["rect"].left <= 0: move_down = True

        if move_down:
            invader_direction *= -1
            lost_life = False
            for inv in invaders:
                inv["rect"].y += invader_drop
                if inv["rect"].top > player_y: lost_life = True
            if lost_life:
                lives -= 1
                if lives <= 0: game_over = True
                else: reset_invaders()

        # Collisions (optimized)
        for b in bullets[:]:
            for inv in invaders[:]:
                if b.colliderect(inv["rect"]):
                    invaders.remove(inv)
                    bullets.remove(b)
                    score += 10 if inv["type"] < 4 else 50
                    break
            else: continue
            break

        if len(invaders) == 0: victory = True

    # Draw
    screen.blit(player_img, (player_x, player_y))
    for b in bullets: screen.blit(bullet_img, (b.x, b.y))
    for inv in invaders: screen.blit(inv["img"], inv["rect"])

    # UI + DEBUG (proves movement!)
    score_text = font.render(f"Score: {score}", True, GOLD)
    lives_text = font.render(f"Lives: {lives}", True, RED)
    debug_text = font.render(f"Invaders: {len(invaders)} | Speed: {invader_speed}", True, WHITE)
    screen.blit(score_text, (10,10))
    screen.blit(lives_text, (WIDTH-200,10))
    screen.blit(debug_text, (10,50))

    # "Merry Christmas" at the TOP of the screen
    # merry_text = font.render("Merry Christmas", True, GOLD)                    # uses normal 36pt font
    # text_rect = merry_text.get_rect(center=(WIDTH // 2, 40))                  # 40 pixels from top
    # pygame.draw.rect(screen, DARK_GREEN, (text_rect.x-15, text_rect.y-8, 
    #                                      text_rect.width+30, text_rect.height+16))
    # pygame.draw.rect(screen, WHITE, (text_rect.x-10, text_rect.y-3, 
    #                                 text_rect.width+20, text_rect.height+6), 2)
    # screen.blit(merry_text, text_rect)
    
        # REAL CHRISTMAS FONT + TWINKLING LIGHTS
    try:
        # Load the real festive font you just uploaded
        festive_font = pygame.font.Font("assets/JandaChristmasDoodles.ttf", 68)
        merry_surf = festive_font.render("Merry Christmas", True, GOLD)
    except:
        # Fallback if something goes wrong
        festive_font = pygame.font.SysFont("comicsansms", 52, bold=True, italic=True)
        merry_surf = festive_font.render("Merry Christmas", True, GOLD)

    merry_rect = merry_surf.get_rect(center=(WIDTH // 2, 50))

    # Soft glow
    glow = pygame.Surface((merry_rect.width + 50, merry_rect.height + 40), pygame.SRCALPHA)
    pygame.draw.rect(glow, (255, 240, 180, 60), glow.get_rect(), border_radius=25)
    screen.blit(glow, (merry_rect.x - 25, merry_rect.y - 20))

    # Draw the real cursive text
    screen.blit(merry_surf, merry_rect)

    # Twinkling lights (same as before — kept because you liked them!)
    light_colors = [(255,0,0), (0,255,0), (255,215,0), (0,255,255), (255,100,200)]
    for i in range(32):
        angle = i * 0.196  # 32 points = perfect circle
        radius = 110 + 12 * math.sin(pygame.time.get_ticks() * 0.004 + i)
        x = WIDTH // 2 + math.cos(angle) * radius
        y = 50 + math.sin(angle) * 45
        brightness = 180 + 75 * math.sin(pygame.time.get_ticks() * 0.007 + i)
        col = light_colors[i % len(light_colors)]
        color = tuple(min(255, int(c * brightness/255)) for c in col)
        pygame.draw.circle(screen, color, (int(x), int(y)), 5)
        pygame.draw.circle(screen, (255,255,180), (int(x), int(y)), 2)
  

    # Tiny "Controls" text at bottom center
    controls_text = font.render("← → Move    Space = Fire", True, (200, 200, 200))  # light gray
    # Make it much smaller
    small_font = pygame.font.SysFont("arial", 18, bold=False)   # 18pt = very small
    controls_surf = small_font.render("← → Move    Space = Fire", True, (220, 220, 220))
    
    controls_rect = controls_surf.get_rect(center=(WIDTH // 2, HEIGHT - 20))  # 20px from bottom
    screen.blit(controls_surf, controls_rect)
    
    # Overlays
    if game_over:
        over_text = big_font.render("GAME OVER", True, RED)
        screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, HEIGHT//2-30)))
        screen.blit(font.render("Press R to Restart", True, WHITE), (WIDTH//2-150, HEIGHT//2+30))
    elif victory:
        win_text = big_font.render("Blitzen the Reindeer & You Have Saved CHRISTMAS from the Bad Grinch! The Skies are Clear!", True, GOLD)
        screen.blit(win_text, win_text.get_rect(center=(WIDTH//2, HEIGHT//2-30)))
        screen.blit(font.render("Press R for More!", True, WHITE), (WIDTH//2-150, HEIGHT//2+30))

    pygame.display.flip()

pygame.quit()
