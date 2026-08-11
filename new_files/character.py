import pygame as pg
import animation as anim

class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y
        
class Character(Position):
    def __init__(self, pos, char_info, scale, last_update):
        super().__init__(pos[0], pos[1])
        self.hp = char_info["hp"]
        self.defense = char_info["defense"]
        self.speed = char_info["speed"]
        self.speed_xy = char_info["speed_xy"]
        self.scale = scale
        self.hitbox_width = char_info["hitbox"][0]*self.scale
        self.hitbox_height = char_info["hitbox"][1]*self.scale
        self.last_update = last_update
    
    def center_char(self, position):
        center = (position[0] + self.hitbox_width//2,  position[1] + self.hitbox_height//2)
        return center

    def draw(self, surface, blit_image, x, y, camera):
        surface.blit(blit_image, (x - camera[0], y - camera[1]))