import random
from os import path
from mlgame.view.view_model import create_asset_init_data


import pygame.sprite
ASSET_PATH = path.join(path.dirname(__file__), "../asset")

class Boss(pygame.sprite.Sprite):
    def __init__(self,level):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([500, 500])
        self.width = 400
        self.height = 200
        self.image = pygame.Surface([self.width, self.height])
        self.color = "#FFEB3B"
        self.rect = self.image.get_rect()
        self.rect.center = (600, 80)
        
        self.dir = 10
        self.bullets = pygame.sprite.Group()
        self.times_up = 3
        self.counter = 0
        self.hp = 100
        self.level = level
        if self.level == 0:
            self.hp = 100
        elif self.level == 1:
            self.hp = 200
        elif self.level == 2:
            self.hp == 300

    def get_bullets(self):
        return self.bullets

    def _gen_bullets(self, count: int = 1, gap:int = 0, y:int = 0, speed:int = 10.5):
        sum = 0
        for i in range(count):
            # add food to group
            bullet = Bullet(self.bullets, self.rect.centerx, self.rect.centery+sum, 0, y, speed)
            sum += gap
        
        
    def _gen_bullets_side(self, count: int = 1, gap:int = 0, y:int = 0, speed:int = 10.5):
        sum = 0
        for i in range(count):
            # add food to group
            bullet = Bullet(self.bullets, self.rect.centerx+self.width/2, self.rect.centery+sum, 0, y, speed)
            bullet = Bullet(self.bullets, self.rect.centerx-self.width/2, self.rect.centery+sum, 0, y, speed)
            sum += gap

    def recycle(self,items):
        for item in items:
            if(item.rect.centery < 0 or item.rect.centery > 720 or item.rect.centerx < 0 or item.rect.centerx >1280):
                items.remove(item)

        return items

    def _fire(self, times_up, b_num, gap, y:int = 0, speed:int = 10.5, side:bool = False):
        if side:
            if(self.counter % times_up == 0):
                self._gen_bullets_side(b_num, gap, y, speed)
        else:
            if(self.counter % times_up == 0):
                self._gen_bullets(b_num, gap, y, speed)
    


    def update(self):
        #body
        self.rect.centerx += self.dir
        if(self.rect.centerx < 0 or self.rect.centerx > 1280):
            self.dir = -self.dir

        #bullet
        self.counter +=1 
        self._fire(3,1, 0)
        if self.level >= 1:
            self._fire(30,30, 7, 300, 30)
        if self.level >= 2:
            self._fire(15,15, 7, 100, 50, True)
        
        self.bullets.update()
        self.recycle(self.bullets)
        


    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }

class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, x, y, dir, speed_up_y:int = 0, speed: int = 10.5):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([8, 8])
        self.color = "#FF0000"
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = 0
        self.dir = dir
        self.speed = 10.5
        self.speed_up_y = speed_up_y
        self.changeSpeed = speed
    

    def update(self) -> None:
        if(self.speed_up_y > 0 and self.rect.centery > self.speed_up_y):
            self.rect.centery += self.changeSpeed
        else:
            self.rect.centery += self.speed

        

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([500, 500])
        self.image = pygame.Surface([8, 8])
        self.color = "#FFEB3B"
        self.rect = self.image.get_rect()
        self.rect.center = (600, 600)
        self.wait = 0

    def get_wait(self):
        return self.wait
    
    def set_wait(self,wait):
        self.wait = wait

    def revival(self,x,y,wait):
        self.rect.centery = y
        self.rect.centerx = x
        self.wait = wait


    def update(self, motions):
        for motion in motions:
            if motion == "UP":
                self.rect.centery -= 10.5
            elif motion == "DOWN":
                self.rect.centery += 10.5
            elif motion == "LEFT":
                self.rect.centerx -= 10.5
            elif motion == "RIGHT":
                self.rect.centerx += 10.5

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }


class Food(pygame.sprite.Sprite):
    def __init__(self, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([8, 8])
        self.color = "#FFFFFF"
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, 800)
        self.rect.centery = random.randint(0, 600)
        self.angle = 0

    def update(self) -> None:
        self.rect.centery -= 10.5

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "ball",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }
