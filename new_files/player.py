import pygame as pg
import character as char
import animation as anim
class Player(char.Character):
    def __init__(self, pos, char_stat, hitbox_info, scale, last_update, tile_size):#last_update is temporary
        super().__init__(pos, char_stat, hitbox_info, scale, last_update)
        print(f"hitbox_width: {self.hitbox_width}")
        print(f"x: {self.x}")
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_size = tile_size[0]
        self.current_anim = anim.player_animations["idle"]
    
    def update_tile_pos(self):
        pass

    def move(self):
        keys = pg.key.get_pressed()
        self.current_anim = anim.player_animations["idle"]

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.y -= self.speed
            self.current_anim = anim.player_animations["run_front"]
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.x -= self.speed
            self.current_anim = anim.player_animations["run_Lside"]
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.y += self.speed
            self.current_anim = anim.player_animations["run_down"]
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.x += self.speed
            self.current_anim = anim.player_animations["run_Rside"]
        