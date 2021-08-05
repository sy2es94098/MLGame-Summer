import random
import pygame

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
    def __init__(self, group, level):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([30,30]) #創建物件的畫布
        self.image.fill(Black)
        pygame.draw.circle(self.image,Gray,(15,15),15,0) #畫布,顏色,(x,y座標),半徑,實心
        self.color = Gray
        self.rect = self.image.get_rect() #取得畫布
        self.rect.x = random.randrange(0,Width-self.rect.width)
        self.rect.y = random.randrange(-100,-50)
        self.level = 0
        self.speedx = 0
        if level == "EASY":
            self.level = 0
            self.speedy = random.randrange(1,3)
        elif level == "NORMAL":
            self.level = 1
            self.speedy = random.randrange(4,6)
        elif level == "HARD":
            self.level = 2
            self.speedy = random.randrange(7,9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > Height:
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
    def __init__(self, group, level):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([25,35])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Army_green, [0,0,25,35], 0)
        self.color = Aymy_green
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,Width-self.rect.width)
        self.rect.y = random.randrange(-120,-60)
        self.speedx = 0
        self.level = 0
        if level == "EASY":
            self.level = 0
            self.speedy = random.randrange(1,3)
        elif level == "NORMAL":
            self.level = 1
            self.speedy = random.randrange(4,6)
        elif level == "HARD":
            self.level = 2
            self.speedy = random.choice((-7,-8,-9,7,8,9))
    
    def shoot(self, count: int = 5, speed: int = 5):
        for i in range(count):
            enemy_bullet = Enemy_bullet_s(self.rect.centerx, self.rect.bottom+5, speed)

    def update(self):
        if self.rect.y < 250: #路線直的之後斜的
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        else:
            self.speedx = 1
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        if self.level == 0:
            self.shoot(5,4)
        elif self.level == 1:
            self.shoot(10,7)
        else:
            self.shoot(10,10)

        if self.rect.bottom > Height:
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
    def __init__(self, group, x, y, speed: int = 5):
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
        if self.rect.bottom > Height:
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
    def __init__(self, group, level):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.Surface([35,35])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Army_dark_green, [0,0,35,35], 0)
        self.color = Army_dark_green
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, Width-self.rect.width)
        self.rect.y = random.randrange(-120,-60)
        self.speedx = 0
        self.level = 0
        if level == "EASY":
            self.level = 0
        elif level == "NORMAL":
            self.level = 1
            self.speedy = random.randrange(2,4)
        elif level == "HARD":
            self.level = 2
            self.speedy = random.randrange(5,7)

    def shoot(self, count: int = 5, speed: int = 5):
        for i in range(count):
            enemy_bullet = Enemy_bullet_b(self.rect.centerx, self.rect.bottom+5, speed)
            enemy_bullet = Enemy_bullet_b(self.rect.centerx+self.widtth/2, self.rect.bottom+5, speed)
            enemy_bullet = Enemy_bullet_b(self.rect.centerx-self.widtth/2, self.rect.bottom+5, speed)
    
    def update(self):
        if self.level == 1:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            self.shoot(5,9)
        elif self.level == 2:
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            self.shoot(10,14)
        
        if self.rect.bottom > Height:
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
        self.image = pygame.Surface([7,7])
        self.image.fill(Black)
        pygame.draw.rect(self.image, Yellow, [0,0,7,7],0)
        self.color = Yellow
        self.rect = self.image.get.rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = speed
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > Height:
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
