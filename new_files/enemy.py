import pygame as pg
import character as char
import animation as anim
import find_path as fp
import random
import convert_to_tiles as ctt 

class Enemy(char.Character):
    def __init__(self, pos, bot_info, scale, last_update, last_atk, tile_size, current_anim):#last_update is temporary
        super().__init__(pos, bot_info, scale, last_update, tile_size, current_anim)
        self.atk = bot_info["attack"]
        self.atk_type = bot_info["attack_type"]
        self.atk_clown = bot_info["attack_cooldown"]
        self.detection_range = bot_info["detection_range"]
        self.attack_range = bot_info["attack_range"]
        self.stop_chase_range = bot_info["stop_range"]
        self.last_atk = last_atk
        self.bot_state = "idle"
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))
        self.init_time = 0
        
    def update_tile_pos(self):
            self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
            self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))

    def spawn_bot(self, world):
         spawn_it = False
         while not spawn_it:
          x, y = random.randint(0, world.world_dim[0] - 1), random.randint(0, world.world_dim[1] - 1)
          if world.world_map[y, x] in range(0, 2):
               xy = ctt.to_cartesian(x, y)
               self.x, self.y = xy[0], xy[1]
               spawn_it = True

    def update_state(self, world_map, current_time):
         Astar = fp.Find_path()

    

        
            