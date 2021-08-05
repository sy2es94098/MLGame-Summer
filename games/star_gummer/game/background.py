
import pygame
import random
#import os

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

WIDTH = 500
HEIGHT = 600
FPS = 60
score = 0
level = 0
life = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("stargunner")
clock = pygame.time.Clock()

#background_img = pygame.image.load(os.path.join("img", "background.jpg")).convert()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_life(surf, lives, x, y):
    for i in range(lives):
        pygame.draw.circle(surf, red, (x + 30*i, y),8, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 8
        self.speedy = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 50:
            self.rect.top = 50
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

#game strating view
def draw_init():
    screen.fill(white)
    Title = pygame.font.Font(None, 100)
    word = pygame.font.Font(None, 60)
    word2 = pygame.font.Font(None, 30)
    textImage = Title.render("StarGunner", True, black)
    screen.blit(textImage, (50, 100))
    pygame.draw.rect(screen, red, [50, 200, 400, 50], 2)
    textImage1 = word.render("Level 1", True, black)
    screen.blit(textImage1, (180, 210))
    pygame.draw.rect(screen, red, [50, 300, 400, 50], 2)
    textImage2 = word.render("Level 2", True, black)
    screen.blit(textImage2, (180, 310))
    pygame.draw.rect(screen, red, [50, 400, 400, 50], 2)
    textImage3 = word.render("Level 3", True, black)
    screen.blit(textImage3, (180, 410))
    textImage4 = word2.render("Please press 1/2/3 to start the game", True, black)
    screen.blit(textImage4, (80, 510))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    level = 1
                    waiting = False
                elif event.key == pygame.K_2:
                    level = 2
                    waiting = False
                elif event.key == pygame.K_3:
                    level = 3
                    waiting = False

#endgame view
def endgame(message, score):
    global running
    screen.fill(white)
    Title = pygame.font.Font(None, 100)
    word = pygame.font.Font(None, 60)
    word2 = pygame.font.Font(None, 30)
    textImage = Title.render(message, True, black)
    screen.blit(textImage, (80, 100))
    text = word.render(str(score), True, black)
    screen.blit(text, (200, 210))
    pygame.draw.rect(screen, red, [50, 300, 400, 50], 2)
    textImage1 = word.render("Menu", True, black)
    screen.blit(textImage1, (200, 310))
    pygame.draw.rect(screen, red, [50, 400, 400, 50], 2)
    textImage2 = word.render("Quit the game", True, black)
    screen.blit(textImage2, (100, 405))
    textImage3 = word2.render("Please press 1(Menu) / 2(Quit)", True, black)
    screen.blit(textImage3, (80, 510))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    waiting = False
                    global show_init
                    show_init = True
                elif event.key == pygame.K_2:
                    pygame.quit()




#game loop
show_init = True
running = True

while running:
    #start view
    if show_init:
        draw_init()
        show_init = False

    clock.tick(FPS)
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #update
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits:
        score += 1
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    attacked = pygame.sprite.spritecollide(player, rocks, True)
    if attacked:
        life -= 1
        if life == 0:
            endgame("Gameover", score)



    #display
    screen.fill(black)
    #screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_life(screen, life, WIDTH-100, 15)
    pygame.display.update()

    #endgame("WIN")

pygame.quit()