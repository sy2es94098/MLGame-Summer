import random
import pygame
from .setting import HEIGHT, WIDTH

FPS = 60

Gray_blue = "#50828b"
Army_green = "#5a7645"
Army_dark_green = "#345501"
Gray = "#b3b3b3"
Black = "#000000"
Red = "#931f1d"
Yellow = "#ca8518"


""" Game objects """
class Enemy_m(pygame.sprite.Sprite): #meteor隕石
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30]) #創建物件的畫布
        self.image.fill(Black)
        pygame.draw.circle(self.image,Gray,(15,15),15,0) #畫布,顏色,(x,y座標),半徑,實心
        self.color = Gray
        self.rect = self.image.get_rect() #取得畫布
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-40,-20)
        self.level = 0
        self.speedx = 0
        self.level = level
        if level == 0:
            self.speedy = random.randrange(4,6)
        elif level == 1:
            self.speedy = random.randrange(6,8)
        elif level == 2:
            self.speedy = random.randrange(8,10)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "Enemy_m",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }


class Enemy_s(pygame.sprite.Sprite): #small enemy:前方1種彈道
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,35])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Army_green, [0,0,25,35], 0)
        self.color = Army_green
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-50,-30)
        self.speedx = random.choice((-5,-4,-3,5,4,3))
        self.level = level
        self.counter = 0
        if level == 0:
            self.speedy = random.randrange(4,6)
        elif level == 1:
            self.speedy = random.randrange(6,8)
        elif level == 2:
            self.speedy = random.randrange(8,10)
        self.bullets = pygame.sprite.Group()
    
    def get_bullets(self):
            return self.bullets

    def shoot(self, count: int = 5, times_up: int = 0, speed: int = 5):
        sum = 0
        if(self.counter % times_up == 0):
            for i in range(count):
                enemy_bullet = Enemy_bullet_s(self.bullets, self.rect.centerx, self.rect.bottom, speed)

    def recycle(self,items):
        for item in items:
            if(item.rect.centery < 0 or item.rect.centery > 600 or item.rect.centerx < 0 or item.rect.centerx > 600):
                items.remove(item)

        return items

    def update(self):
        self.counter += 1
        if self.rect.y < 100: #路線直的之後斜的
            self.rect.x += 0
            self.rect.y += self.speedy
        else:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        if self.level == 0:
            self.shoot(1, 5, 10)
        elif self.level == 1:
            self.shoot(1, 5, 13)
        else:
            self.shoot(1, 5, 15)
        
        # self.bullets.update()
        #self.recycle(self.bullets)
        if self.rect.bottom > HEIGHT:
            self.kill()

    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "Enemy_s",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }


class Enemy_bullet_s(pygame.sprite.Sprite):
    def __init__(self,group , x, y, speed: int = 5):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([5,5])
        self.image.fill(Black)
        pygame.draw.rect(self.image,Red,[0,0,5,5],0)
        self.color = Red
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = speed
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill() 
    
    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "Enemy_bullet_s",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }

class Enemy_b(pygame.sprite.Sprite): #big enemy:前方三種彈道
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([35,35])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Army_dark_green, [0,0,35,35], 0)
        self.color = Army_dark_green
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH-self.rect.width)
        self.rect.y = random.randrange(-50,-30)
        self.speedx = 0
        self.counter = 0
        self.level = level
        if level == 1:
            self.speedy = random.randrange(3,5)
        elif level == 2:
            self.speedy = random.randrange(5,7)
        self.bullets = pygame.sprite.Group()
    
    def recycle(self,items):
        for item in items:
            if(item.rect.centery < 0 or item.rect.centery > 600 or item.rect.centerx < 0 or item.rect.centerx > 600):
                items.remove(item)

        return items

    def get_bullets(self):
            return self.bullets

    def shoot(self, count: int = 5, times_up: int = 0, speed: int = 5):
        sum = 0
        if(self.counter % times_up == 0):
            for i in range(count):
                enemy_bullet = Enemy_bullet_b(self.bullets, self.rect.centerx, self.rect.bottom+sum, speed)
                enemy_bullet = Enemy_bullet_b(self.bullets, self.rect.centerx+self.rect.width/2-10, self.rect.bottom+sum, speed)
                enemy_bullet = Enemy_bullet_b(self.bullets, self.rect.centerx-self.rect.width/2+10, self.rect.bottom+sum, speed)

    def update(self):
        self.counter += 1
        if self.level == 1:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            self.shoot(1, 7, 10)
        elif self.level == 2:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            self.shoot(1, 7, 14)
        
        #self.bullets.update()
        #self.recycle(self.bullets)
        if self.rect.bottom > HEIGHT:
            self.kill()
    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "Enemy_b",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }
    
class Enemy_bullet_b(pygame.sprite.Sprite):
    def __init__(self, group, x, y, speed: int = 5):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([6,6])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Yellow, [0,0,6,6],0)
        self.color = Yellow
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = speed
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill() 
    
    @property
    def game_object_data(self):
        return {"type": "rect",
                "name": "Enemy_bullet_b",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "color": self.color
                }


#敵人不能彼此覆蓋到
#Level 0: Enemy_m 3個, Enemy_s:3個  
#Level 1: Enemy_m 3個, Enemy_s:3個, Enemy_b:2個 (Enemy_b要被擊中兩次才會死)
#Level 2: Enemy_m 5個, Enemy_s:3個, Enemy_b:3個 (Enemy_b要被擊中兩次才會死)