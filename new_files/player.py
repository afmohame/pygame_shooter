import pygame as pg
import character as char
import animation as anim

class Player(char.Character):
    def __init__(self, pos, player_info, scale, last_update, tile_size):#last_update is temporary
        super().__init__(pos, player_info, scale, last_update)
        print(f"hitbox_width: {self.hitbox_width}")
        print(f"x: {self.x}")
        self.stamina = player_info["stamina"]
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_size = tile_size[0]
        self.current_anim = anim.player_animations["idle"]
    
    def update_tile_pos(self):
        self.current_tile = (self.x//self.tile_size, self.y//self.tile_size)
        print(f"this is my current position: {(self.x, self.y)}")
        print(f"this is my current tile position: {self.current_tile}")
    
    def sprint(self):
        key = pg.key.get_pressed()
        if key[pg.K_LSHIFT]:
            pass
    
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
                if (W and A):
                    self.current_anim = anim.player_animations["run_Lside"]
                    if world_map.is_walkable((self.x, self.y), (-self.speed_xy, 0), (self.hitbox_width, self.hitbox_height)):
                        self.x -= self.speed_xy
                    if world_map.is_walkable((self.x, self.y), (0, -self.speed_xy), (self.hitbox_width, self.hitbox_height)):
                        self.y -= self.speed_xy
                if (W and D):
                    self.current_anim = anim.player_animations["run_Rside"]
                    if world_map.is_walkable((self.x, self.y), (self.speed_xy, 0), (self.hitbox_width, self.hitbox_height)):
                        self.x += self.speed_xy
                    if world_map.is_walkable((self.x, self.y), (0, -self.speed_xy), (self.hitbox_width, self.hitbox_height)):
                        self.y -= self.speed_xy
                if (S and A):
                    self.current_anim = anim.player_animations["run_Lside"]
                    if world_map.is_walkable((self.x, self.y), (-self.speed_xy, 0), (self.hitbox_width, self.hitbox_height)):
                        self.x -= self.speed_xy
                    if world_map.is_walkable((self.x, self.y), (0, self.speed_xy), (self.hitbox_width, self.hitbox_height)):
                        self.y += self.speed_xy
                if (S and D):
                    self.current_anim = anim.player_animations["run_Rside"]
                    if world_map.is_walkable((self.x, self.y), (self.speed_xy, 0), (self.hitbox_width, self.hitbox_height)):
                        self.x += self.speed_xy
                    if world_map.is_walkable((self.x, self.y), (0, self.speed_xy), (self.hitbox_width, self.hitbox_height)):
                        self.y += self.speed_xy
    
            if not movexy[0] and movexy[1]:
                if W and world_map.is_walkable((self.x, self.y), (0, -self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.current_anim = anim.player_animations["run_front"]
                    self.y -= self.speed
                if S and world_map.is_walkable((self.x, self.y), (0, self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.current_anim = anim.player_animations["run_down"]
                    self.y += self.speed
            if movexy[0] and not movexy[1]:
                if A and world_map.is_walkable((self.x, self.y), (-self.speed, 0), (self.hitbox_width, self.hitbox_height)):
                    self.current_anim = anim.player_animations["run_Lside"]
                    self.x -= self.speed
                if D and world_map.is_walkable((self.x, self.y), (self.speed, 0), (self.hitbox_width, self.hitbox_height)):
                    self.current_anim = anim.player_animations["run_Rside"]
                    self.x += self.speed