import time
import random
import pygame
from .boss import Boss
from .enemies import Enemy_m, Enemy_s, Enemy_bullet_s, Enemy_b, Enemy_bullet_b
from .player import Player
from .prop.prop import Prop
from .prop.buff import *
from mlgame.gamedev.game_interface import PaiaGame, GameResultState, GameStatus
from mlgame.view.test_decorator import check_game_progress, check_game_result
from mlgame.view.view_model import create_text_view_data, create_asset_init_data, create_image_view_data, create_rect_view_data,Scene
from os import path
from .setting import *
import numpy as np
import mlgame.global_variable as gv


ASSET_PATH = path.join(path.dirname(__file__), "../assets")


class Star_Gummer(PaiaGame):
    def __init__(self,level = "EASY"):
        super().__init__()
        self.game_result_state = GameResultState.FAIL
        self.scene = Scene(width=WIDTH, height=HEIGHT, color="#000000", bias_x=0, bias_y=0)
        self.frame_count = 0
        self.level = level
        self.player = Player(self)
        self.boss = None
        self.encounter = False
        self.enemy_m = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.level = 0
        self.bullets = pygame.sprite.Group()
        self.return_bullet = []
        self.return_enemy = []
        self.return_meteor = []
        self.return_props = []
        #self.pixels = np.zeros(360000, dtype=np.float)
        if level == "EASY":
            self.level = 0
        elif level == "NORMAL":
            self.level = 1
        elif level == "HARD":
            self.level = 2
        self.props = []
        self.reward = 0
        #self.pixels = []

    def update(self, commands):
        self.frame_count += 1
        self.pixels = gv.pixels
        get_buff = False
        get_hit = False
        if self.frame_count % 300 == 0:
            buff = random.choice([RecoverBuff(), WSPBuff(), AttackBuff(), RangeBuff()])
            self.props.append(Prop(random.randint(0, WIDTH), random.randint(0, HEIGHT), buff))
        for prop in self.props:
            if prop.is_collide(self.player):
                prop.buff.buff(self.player)
                get_buff = True
                self.props.remove(prop)

        if self.frame_count % 100 == 0:
            if self.level == 0:
                for i in range(2):
                    e1 = Enemy_m(self.level)
                    self.enemy_m.add(e1)
                for i in range(2):
                    e2 = Enemy_s(self.level)
                    self.enemies.add(e2)
            elif self.level == 1:
                for i in range(2):
                    e1 = Enemy_m(self.level)
                    self.enemy_m.add(e1)
                for i in range(2):
                    e2 = Enemy_s(self.level)
                    self.enemies.add(e2)
                for i in range(1):
                    e3 = Enemy_b(self.level)
                    self.enemies.add(e3)
            elif self.level == 2:
                for i in range(3):
                    e1 = Enemy_m(self.level)
                    self.enemy_m.add(e1)
                for i in range(3):
                    e2 = Enemy_s(self.level)
                    self.enemies.add(e2)
                for i in range(2):
                    e3 = Enemy_b(self.level)
                    self.enemies.add(e3)

        self.enemies.update()
        for enemy in self.enemies:
            for bullet in enemy.get_bullets():
                self.bullets.add(bullet)
        self.player.update(commands["1P"])
        self.enemy_m.update()

        if self.frame_count >= 600 and self.boss == None:
            self.boss = Boss(self.level)
            self.encounter = True

        if self.encounter:
            self.boss.update()
            for bullet in self.boss.get_bullets():
                self.bullets.add(bullet)
            hits = pygame.sprite.spritecollide(self.boss, self.player.bullets, True)
            for hit in hits:
                self.boss.hp -= 1
                get_hit = True
        
        hits = pygame.sprite.spritecollide(self.player, self.enemy_m, True)
        for hit in hits:
            #print(self.player.hp)
            self.player.hp -= 1
            get_hit = True
            #self.reward = -1

        self.bullets.update()
        pygame.sprite.groupcollide(self.player.bullets, self.enemies, True, True)
        self.recycle(self.bullets)
        self.collect_return_data()

        if get_hit:
            self.reward = -1
        elif get_buff:
            self.reward = 0.5
        else:
            self.reward = 0.1

        if not self.is_running:
            return "QUIT"

    def recycle(self,items):
        for item in items:
            if(item.rect.centery < 0 or item.rect.centery > 600 or item.rect.centerx < 0 or item.rect.centerx > 600):
                items.remove(item)

        return items

    def collect_return_data(self):
        self.return_enemy = []
        self.return_meteor = []
        self.return_bullet = []
        self.return_props = []
        for enemy in self.enemies:
            self.return_enemy.append(enemy.game_object_data)

        for enemy in self.enemy_m:
            self.return_meteor.append(enemy.game_object_data)

        for bullet in self.bullets:
            self.return_bullet.append(bullet.game_object_data)

        for prop in self.props:
            self.return_props.append(create_rect_view_data("prop", prop.rect[0], prop.rect[1],
                                      PROP_SIZE[0], PROP_SIZE[1], GREEN))

    def game_to_player_data(self):
        """
        send something to game AI
        we could send different data to different ai
        """
        player_info = self.player.get_info()
        data =create_rect_view_data("player", player_info["pos"][0], player_info["pos"][1],player_info["size"][0], player_info["size"][1], "#FFFFF0")
        try:
            to_players_data = {'1P' : [{"player": data,
            "reward": self.reward, "frames": self.frame_count, "state": self.get_game_status(),
            "enemies":self.return_enemy,"meteor":self.return_meteor,"bullets":self.return_bullet,
            "boss":self.boss.game_object_data, 'props' : self.return_props}]}
        except:
            to_players_data = {'1P' : [{"player": data,
            "reward": self.reward, "frames": self.frame_count,"state": self.get_game_status(),
            "enemies":self.return_enemy,"meteor":self.return_meteor,"bullets":self.return_bullet,
            "boss":[], 'props' : self.return_props}]}


        #,{'enemy':}
        # should be equal to config. GAME_SETUP["ml_clients"][0]["name"]

        return to_players_data

    def write_result(self,file,res):
        with open(file,'a') as f:
            f.write(res + "\n")

    def get_game_status(self):
        if self.game_alive():
            status = GameStatus.GAME_ALIVE
        elif self.player.hp  > 0:
            status = GameStatus.GAME_PASS
            self.write_result(path.join("./","result.txt"),"1")
            self.reward = 5
            self.reset()
        else:
            status = GameStatus.GAME_OVER
            self.write_result(path.join("./","result.txt"),"0")
            self.reward = -5
            self.reset()
        return status

    def reset(self):
        del self.player
        del self.boss
        del self.enemy_m
        del self.enemies
        del self.bullets

        self.game_result_state = GameResultState.FAIL
        self.frame_count = 0
        self.player = Player(self)
        self.boss = None
        self.encounter = False
        self.enemy_m = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.level = 0
        self.bullets = pygame.sprite.Group()
        self.return_bullet = []
        self.return_enemy = []
        self.return_meteor = []
        self.return_props = []
        self.props = []
        
    def game_alive(self):
        if self.player.hp <=0:
            return False
        try:
            if self.boss.hp <=0:
                return False
        except Exception:
            pass
        return True

    @property
    def is_running(self):
        return True
    
    def conf_img(self, relate_path, name, width, height):
        pic = path.join(ASSET_PATH, relate_path)
        conf = create_asset_init_data(name, width, height, pic, "url")

        return conf

    def get_scene_init_data(self):
        """
        Get the initial scene and object information for drawing on the web
        """
        # TODO add music or sound
        boss1 = self.conf_img("boss/boss1.png", "boss1", 200, 100)
        boss2 = self.conf_img("boss/boss2.png", "boss2", 150, 200)
        boss3 = self.conf_img("boss/boss3.png", "boss3", 200, 100)

        scene_init_data = {"scene": self.scene.__dict__,
                           "assets": [
                               boss1,
                               boss2,
                               boss3,
                           ],
                           # "audios": {}
                           }
        return scene_init_data

        # scene_init_data = {"scene": self.scene.__dict__,
        #                    "assets": [],
        #                    # "audios": {}
        #                    }
        # return scene_init_data

    @check_game_progress
    def get_scene_progress_data(self):
        """
        Get the position of game objects for drawing on the web
        """
        scene_progress = {
            # background view data will be draw first
            "background": [

            ],
            # game object view data will be draw on screen by order , and it could be shifted by WASD
            "object_list": [],
            "toggle": [],
            "foreground": [],
            # other information to display on web
            "user_info": [],
            # other information to display on web
            "game_sys_info": {}
        }
        player_info = self.player.get_info()
        scene_progress["object_list"].append(create_rect_view_data("player", player_info["pos"][0], player_info["pos"][1],
                                                                   player_info["size"][0], player_info["size"][1], "#FFFFF0"))
        for bullet in player_info["bullets_pos"]:
            scene_progress["object_list"].append(
                create_rect_view_data("bullet", bullet[0], bullet[1],
                                      BULLET_SIZE[0],BULLET_SIZE[1], YELLOW))
        for prop in self.props:
            scene_progress["object_list"].append(
                create_rect_view_data("prop", prop.rect[0], prop.rect[1],
                                      PROP_SIZE[0], PROP_SIZE[1], GREEN))
        try:
            scene_progress["object_list"].append(self.boss.game_object_data)
        except:
            pass
        
        for enemy in self.enemies:
            scene_progress["object_list"].append(enemy.game_object_data)

        for enemy in self.enemy_m:
            scene_progress["object_list"].append(enemy.game_object_data)

        for bullet in self.bullets:
            scene_progress["object_list"].append(bullet.game_object_data)
        

        
        
  
        return scene_progress

    @check_game_result
    def get_game_result(self):
        """
        send game result
        """
    
        if self.get_game_status() == GameStatus.GAME_PASS:
            self.game_result_state = GameResultState.FINISH
        return {"frame_used": self.frame_count,
                "state": self.game_result_state,
                "ranks":[],
                "attachment": 
                    {"player":self.ai_clients()[0]["name"],
                    }
                }

        pass

    def get_keyboard_command(self):
        """
        Define how your game will run by your keyboard
        """
        cmd_1p = []
        key_pressed_list = pygame.key.get_pressed()
        if key_pressed_list[pygame.K_UP]:
            cmd_1p.append(SPEED_cmd)
        if key_pressed_list[pygame.K_DOWN]:
            cmd_1p.append(BRAKE_cmd)

        if key_pressed_list[pygame.K_LEFT]:
            cmd_1p.append(LEFT_cmd)

        if key_pressed_list[pygame.K_RIGHT]:
            cmd_1p.append(RIGHT_cmd)
        ai_1p = self.ai_clients()[0]["name"]
        return {ai_1p: cmd_1p}


    @staticmethod
    def ai_clients():
        """
        let MLGame know how to parse your ai,
        you can also use this names to get different cmd and send different data to each ai client
        """
        return [
            {"name": "1P"}
        ]
