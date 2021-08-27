from os import path
import pygame.sprite

class Boss(pygame.sprite.Sprite):
    def __init__(self,level):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface([500, 500])
        self.width = 200
        self.height = 100
        self.level = 0
        self.id = "boss1"
        if level == 0:
            self.width = 200
            self.height = 100
            self.hp = 30
            self.level = 0
            self.id = "boss1"
        elif level == 1:
            self.width = 150
            self.height = 200
            self.hp = 60
            self.level = 1
            self.id = "boss2"
        elif level == 2:
            self.width = 200
            self.height = 100
            self.hp = 90
            self.level = 2
            self.id = "boss3"

        self.image = pygame.Surface([self.width, self.height])
        self.color = "#FFEB3B"
        self.rect = self.image.get_rect()
        self.rect.center = (600, 80)
        
        self.dir = 10
        self.bullets = pygame.sprite.Group()
        self.times_up = 3
        self.counter = 0
        self.hp = 100
        


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
            if(item.rect.centery < 0 or item.rect.centery > 600 or item.rect.centerx < 0 or item.rect.centerx > 600):
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
        self._fire(10,1, 0)
        if self.level >= 1:
            self._fire(30,30, 7, 300, 30)
        if self.level >= 2:
            self._fire(15,15, 7, 100, 50, True)
        
        #self.recycle(self.bullets)
        

    @property
    def game_object_data(self):
        return {"type": "image",
                "x": self.rect.x,
                "y": self.rect.y,
                "angle": 0,
                "width": self.rect.width,
                "height": self.rect.height,
                "image_id": self.id
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
