import pygame as pg
import character as char
import animation as anim
class Player(char.Character):
    def __init__(self, pos, char_stat, hitbox_info, scale, last_update, tile_size):#last_update is temporary
        super().__init__(pos, char_stat, hitbox_info, scale, last_update)
        print(f"hitbox_width: {self.hitbox_width}")
        print(f"x: {self.x}")
        self.stamina = char_stat["stamina"]
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_size = tile_size[0]
        self.current_anim = anim.player_animations["idle"]
    
    def update_tile_pos(self):
        pass
    
    def sprint(self):
        key = pg.key.get_pressed()
        if key[pg.K_LSHIFT]:
            pass
        

    def move(self):
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
            if W and A:
                self.current_anim = anim.player_animations["run_Lside"]
                self.x -= self.speed_xy
                self.y -= self.speed_xy
            if W and D:
                self.current_anim = anim.player_animations["run_Rside"]
                self.x += self.speed_xy
                self.y -= self.speed_xy
            if S and A:
                self.current_anim = anim.player_animations["run_Lside"]
                self.x -= self.speed_xy
                self.y += self.speed_xy
            if S and D:
                self.current_anim = anim.player_animations["run_Rside"]
                self.x += self.speed_xy
                self.y += self.speed_xy

        if not movexy[0] and movexy[1]:
            if W:
                self.current_anim = anim.player_animations["run_front"]
                self.y -= self.speed
            if S:
                self.current_anim = anim.player_animations["run_down"]
                self.y += self.speed
        if movexy[0] and not movexy[1]:
            if A:
                self.current_anim = anim.player_animations["run_Lside"]
                self.x -= self.speed
            if D:
                self.current_anim = anim.player_animations["run_Rside"]
                self.x += self.speed