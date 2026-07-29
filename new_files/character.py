import pygame as pg
import animation as anim
import collision as coll

class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y
        
class Character(Position):
    def __init__(self, pos, char_stat, hitbox_info, scale, last_update):
        super().__init__(pos[0], pos[1])
        self.hp = char_stat["hp"]
        self.defense = char_stat["defense"]
        self.speed = char_stat["speed"]
        self.speed_xy = char_stat["speed_xy"]
        self.scale = scale
        self.hitbox_width = hitbox_info["width"]*self.scale
        self.hitbox_height = hitbox_info["height"]*self.scale
        self.last_update = last_update
    
    def center_char(self, position):
        center = (position[0] + self.hitbox_width//2,  position[1] + self.hitbox_height//2)
        return center

    def move(self, world_map):
            keys = pg.key.get_pressed()
            self.current_anim = anim.player_animations["idle"]
            W, A, S, D = None, None, None, None
            movexy = [False, False]
    
            if keys[pg.K_UP] or keys[pg.K_w]:
                W = True
                movexy[1] = True
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                A = True
                movexy[0] = True
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                S = True
                movexy[1] = True
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                D = True
                movexy[0] = True
            
            if movexy[0] and movexy[1]:
                if (W and A) and world_map.is_walkable((self.x, self.y), self.speed_xy, "WA"):
                    self.current_anim = anim.player_animations["run_Lside"]
                    #self.rect = 
                    self.x -= self.speed_xy
                    self.y -= self.speed_xy
                if (W and D) and world_map.is_walkable((self.x, self.y), self.speed_xy, "WD"):
                    self.current_anim = anim.player_animations["run_Rside"]
                    self.x += self.speed_xy
                    self.y -= self.speed_xy
                if (S and A) and world_map.is_walkable((self.x, self.y), self.speed_xy, "SA"):
                    self.current_anim = anim.player_animations["run_Lside"]
                    self.x -= self.speed_xy
                    self.y += self.speed_xy
                if (S and D) and world_map.is_walkable((self.x, self.y), self.speed_xy, "SD"):
                    self.current_anim = anim.player_animations["run_Rside"]
                    self.x += self.speed_xy
                    self.y += self.speed_xy
    
            if not movexy[0] and movexy[1]:
                if W and world_map.is_walkable((self.x, self.y), self.speed, "W"):
                    self.current_anim = anim.player_animations["run_front"]
                    self.y -= self.speed
                if S and world_map.is_walkable((self.x, self.y), self.speed, "S"):
                    self.current_anim = anim.player_animations["run_down"]
                    self.y += self.speed
            if movexy[0] and not movexy[1]:
                if A and world_map.is_walkable((self.x, self.y), self.speed, "A"):
                    self.current_anim = anim.player_animations["run_Lside"]
                    self.x -= self.speed
                if D and world_map.is_walkable((self.x, self.y), self.speed, "D"):
                    self.current_anim = anim.player_animations["run_Rside"]
                    self.x += self.speed

    def draw_char(self, surface, blit_image, x, y, camera):
        surface.blit(blit_image, (x - camera[0], y - camera[1]))