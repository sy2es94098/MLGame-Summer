import pygame
from games.star_gummer.game.setting import *

class Prop:
    def __init__(self, x, y, buff):
        self.image = pygame.Surface(PROP_SIZE)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.buff = buff

    def is_collide(self, player):
        if self.rect.colliderect(player.rect):
            print(self.buff)
            return True
        return False
