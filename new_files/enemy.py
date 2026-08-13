import pygame as pg
import character as char
import cte
import animation as anim
import find_path as fp
import random
import math
import projectile
import convert_to_tiles as ctt 

class Enemy(char.Character):
    def __init__(self, pos, bot_info, scale, last_update, last_atk, tile_size, current_anim, proj_img):#last_update is temporary
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
        self.proj_img = proj_img
        
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


    def update_state(self, player, world_map, current_time, proj_info):
        dx, dy = self.x - player.x, self.y - player.y
        distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        if distance <= self.detection_range:
            ### RETREAT ###
            if distance <= self.stop_chase_range:
                self.bot_state = "retreat"
                move_x, move_y = abs(dx) > self.speed, abs(dy) > self.speed #checks if bot needs to move, return a bool

                if move_x and move_y:
                    speed = self.speed_xy
                else:
                    speed = self.speed

                if move_x:
                    if dx > 0:
                        if self.move_allowed(world_map, (speed, 0)):
                            self.x += speed
                    else:
                        if self.move_allowed(world_map, (speed, 0)):
                            self.x -= speed

                if move_y:
                    if dy > 0:
                        if self.move_allowed(world_map, (0, speed)):
                            self.y += speed
                    else:
                        if self.move_allowed(world_map, (0, speed)):
                            self.y -= speed
                        
            ### ATTACK ###
            if distance <= self.attack_range:
                self.bot_state = "attack"

                if current_time - self.last_atk >= self.atk_clown:
                    proj = projectile.Projectile(self.center, proj_info, (player.center), current_time)
                    cte.list_of_enemy_projectile.append(proj)
                    self.last_atk = current_time

            ### CHASE ###
            else:
                self.bot_state = "chase"
                path_player = fp.Find_path(world_map)
                the_path = path_player.find_it((self.x, self.y), (player.x, player.y))


                if len(the_path) >= 2:
                    next_tile = the_path[1]
                    next_pos = ctt.to_cartesian(next_tile[0], next_tile[1])

                    cdx, cdy = next_pos[0] - self.x, next_pos[1] - self.y
                    move_x, move_y = abs(cdx) > self.speed, abs(cdy) > self.speed #checks if bot needs to move each axis

                    if move_x and move_y:
                        speed = self.speed_xy
                    else:
                        speed = self.speed
                    
                    if move_x:
                        if cdx > 0:
                            if self.move_allowed(world_map, (speed, 0)):
                                self.x += speed
                        else:
                            if self.move_allowed(world_map, (-speed, 0)):
                                self.x -= speed
                    
                    if move_y:
                        if cdy > 0:
                            if self.move_allowed(world_map, (0, speed)):
                                self.y += speed
                        else:
                            if self.move_allowed(world_map, (0, -speed)):
                                self.y -= speed

        else:
            self.bot_state = "idle"

        self.update_tile_pos()



    

        
            