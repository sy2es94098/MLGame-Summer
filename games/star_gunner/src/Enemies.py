import random
import pygame

FPS = 60

Gray_blue = (85,130,139)
Army_green = (52,85,1)
Gray = (179,179,179)
Black = (0,0,0)
Red = (147,31,29)

pygame.init()

"""設定視窗"""
Width, Height = 480, 600
screen = pygame.display.set_mode((Width, Height)) 

"""建立畫布bg"""
bg = pygame.Surface(screen.get_size()) 
bg = bg.convert() #convert()建立副本, 加快畫布在視窗顯示速度
bg.fill(Black)


""" Game objects """
class Enemy_m(pygame.sprite.Sprite): #meteor隕石
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30,30]) #創建物件的畫布
        self.image.fill(Black)
        pygame.draw.circle(self.image,Gray,(15,15),15,0) #畫布,顏色,(x,y座標),半徑,實心
        self.rect = self.image.get_rect() #取得畫布
        self.rect.x = random.randrange(0,Width-self.rect.width)
        self.rect.y = 0
        self.speedx = 0
        self.speedy = random.randrange(1,5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #???????超出介面
    
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


class Enemy_s(pygame.sprite.Sprite): #small敵人1發子彈
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([25,35])
        self.image.fill(Black)
        pygame.draw.rect(self.image,Army_green,[0,0,25,35],0)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,Width-self.rect.width)
        self.rect.y = 0
        self.speedx = 0
        self.speedy = random.randrange(1,8)
    
    def shoot(self):
        enemy_bullet = Enemy_bullet_s(self.rect.centerx,self.rect.bottom+5)
        all_sprites.add(enemy_bullet)
        enemy_bullets.add(enemy_bullet)

    def update(self):
        if self.rect.y < 250: #路線直的之後斜的
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        else:
            self.speedx = 1
            self.rect.x += self.speedx
            self.rect.y += self.speedy
        
        self.shoot()


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


class Enemy_bullet_s(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5,5])
        self.image.fill(Black)
        pygame.draw.rect(self.image,Red,[0,0,5,5],0)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > Height:
            self.kill() 
    
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

   
all_sprites = pygame.sprite.Group()

enemies_m = pygame.sprite.Group()
for i in range(3):
    e1 = Enemy_m()
    all_sprites.add(e1)
    enemies_m.add(e1)

enemies = pygame.sprite.Group()
for i in range(3):
    e2 = Enemy_s()
    all_sprites.add(e2)
    enemies.add(e2)

enemy_bullets = pygame.sprite.Group()


#待修改: 1.敵人撞到自己子彈 2.敵人重疊 3. 設計第二個敵人(三個方向的子彈)

""" Game loop """


running = True
while running:
    pygame.time.Clock().tick(FPS) #keeping running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    


    all_sprites.update() #update

    # checking if a bullet hits an enemy
    # hits = pygame.sprite.groupcollide(enemies_m, bullets, True, True) #True值為要從group移除
    # for hit in hits:
    #     new_enemy()

    # checking if an enemy hits the player
    # hits = pygame.sprite.spritecllide(player, enemies_c, False)
    # for hit in hits:
    # player #減一條命

    # rendering
    screen.blit(bg,(0,0)) #視窗變數.blit(背景變數, 繪製位置)  #繪製覆蓋整個視窗
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()


  
