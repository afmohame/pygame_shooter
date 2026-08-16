import pygame as pg
import animation as anim
import cte
import world

class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y
        
class Character(Position):
    def __init__(self, pos, char_info, scale, last_update, tile_size, current_anim):
        super().__init__(pos[0], pos[1])
        self.hp = char_info["hp"]
        self.defense = char_info["defense"]
        self.speed = char_info["speed"]
        self.speed_xy = char_info["speed_xy"]
        self.scale = scale
        self.hitbox_width = char_info["hitbox"][0]*self.scale
        self.hitbox_height = char_info["hitbox"][1]*self.scale
        self.hitbox_offset_x = char_info["hitbox_offset"][0]*scale
        self.hitbox_offset_y = char_info["hitbox_offset"][1]*scale
        self.last_update = last_update
        self.current_anim = current_anim
        self.frame = 0
        self.tile_size = tile_size
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)

    def update_tile_pos(self):
            self.center_tile = (self.x + self.hitbox_offset_x + self.hitbox_width//2, 
                                self.y + self.hitbox_offset_y + self.hitbox_height//2)
            self.current_tile = (self.x//self.tile_size, self.y//self.tile_size)
    
    def update_center_char(self):
        self.center = (self.x + self.hitbox_width//2 + self.hitbox_offset_x,
                       self.y + self.hitbox_height//2 + self.hitbox_offset_y)

    def take_damage(self, atk):
        self.hp -= atk
        print(f"his live is {self.hp}")

    def move_allowed(self, world, speed):
        if world.is_walkable((self.x + self.hitbox_offset_x, self.y + self.hitbox_offset_y), speed, 
                             (self.hitbox_width + self.hitbox_offset_x, self.hitbox_height + self.hitbox_offset_x)):
            return True
        return False
    
    def dead(self):
        if self.hp <= 0:
            return True
        return False
        
    def draw(self, surface, blit_image, camera):
        surface.blit(blit_image, (self.x - camera[0], self.y - camera[1]))
    