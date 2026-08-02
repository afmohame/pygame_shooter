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

    def draw(self, surface, blit_image, x, y, camera):
        surface.blit(blit_image, (x - camera[0], y - camera[1]))