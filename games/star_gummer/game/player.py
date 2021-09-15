import pygame
from .setting import *
from .bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface(PLAYER_SIZE)
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = 220, 560
        self.hp = 30
        self.range = 1
        self.speed = 10
        self.attack = 3
        self.wsp = 6
        self.max_wsp = 12
        self.last_attack = 0
        self.frame = 0
        self.bullets = pygame.sprite.Group()
        pass

    def update(self, cmd:list) -> None:
        self.move(cmd)
        self.keep_is_scream()
        self.frame += 1
        if self.frame - self.last_attack > self.max_wsp - self.wsp:
            for i in range(self.range):
                self.shoot(self.rect.centerx + i*5)
            self.last_attack = self.frame
        self.bullets.update()
        self.get_hurt(self.game.bullets)
        
        pass

    def get_info(self):
        player_info = {
            "pos":(self.rect.x, self.rect.y),
            "color":"#FFFFF0",
            "size":(self.rect.width, self.rect.height),
            "bullets_pos":[],
        }

        for bullet in self.bullets:
            player_info["bullets_pos"].append(bullet.rect.topleft)

        return player_info

    def move(self, cmd:list):
        if cmd == None:
            return True
        if LEFT_cmd in cmd:
            self.rect.x -= self.speed
        if RIGHT_cmd in cmd:
            self.rect.x += self.speed
        if SPEED_cmd in cmd:
            self.rect.y -= self.speed
        elif BRAKE_cmd in cmd:
            self.rect.y += self.speed
        else:
            pass

    def shoot(self, x:int):
        bullet = Bullet(x, self.rect.top)
        self.bullets.add(bullet)

    def get_hurt(self, bullets):
        hits = pygame.sprite.spritecollide(self, bullets, True)
        for hit in hits:
            print(self.hp)
            self.hp -= 1
    
        

    def keep_is_scream(self):
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
