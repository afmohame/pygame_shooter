import pygame as pg
import character as char
import animation as anim
import collision as coll
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
        self.current_tile = (self.x//self.tile_size, self.y//self.tile_size)
        print(f"this is my current position: {(self.x, self.y)}")
        print(f"this is my current tile position: {self.current_tile}")
    
    def sprint(self):
        key = pg.key.get_pressed()
        if key[pg.K_LSHIFT]:
            pass