import pygame as pg
import numpy as np

class World():
    def __init__(self, world_dim, floor, destr_wall, outer_wall, tile_size):
        self.world_width, self.world_height = world_dim[0], world_dim[1]
        self.floor, self.destr_wall, self.outer_wall = floor, destr_wall, outer_wall
        self.tile_size = tile_size
        self.tile_type = {
            0: self.floor, #walkable
            1: self.destr_wall, #not walkable
            2: self.outer_wall #not walkable
}
        self.world_map = np.full((self.world_height, self.world_width), 2, dtype = int)

    def generate_world(self):
        self.world_map[1:-1, 1:-1] = np.random.choice(
            [0, 1], #number(s) to randomly disperse in the room
            size = (self.world_height - 2, self.world_width - 2), #boundaries where to disperse them
            p = [0.8, 0.2] #probabilities of 0 and 1 respectively
        )
        self.world_map[1:4, 1:4] = 0 #where the player will spawn

    def get_world(self):
        return self.world_map
    
    def place_char(self):
        pass

    def move_allowed(self, char_pos, char_hitbox):#modulo geeft rest -> niet gebruiken
        hitbox = {"left": char_pos[0], "right": char_pos[0] + char_hitbox[0] - 1, "top": char_pos[1], "bottom": char_pos[1] + char_hitbox[1] - 1}
        #TOP LEFT
        tile_x = (hitbox["left"])//self.tile_size #gives which tile I am on
        tile_y = (hitbox["top"])//self.tile_size #gives which tile I am on
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #TOP RIGHT
        tile_x = (hitbox["right"])//self.tile_size
        tile_y = (hitbox["top"])//self.tile_size
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #BOTTOM LEFT
        tile_x = (hitbox["left"])//self.tile_size
        tile_y = (hitbox["bottom"])//self.tile_size
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #BOTTOM RIGHT
        tile_x = (hitbox["right"])//self.tile_size
        tile_y = (hitbox["bottom"])//self.tile_size
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        return True

    def draw_world(self, surface, camera):
        row_indx, column_indx = 0, 0
        for row in self.world_map:
            for column in row:
                x = column_indx*self.tile_size - camera[0]
                y = row_indx*self.tile_size - camera[1]
                if column == 0:
                    surface.blit(self.tile_type[0], (x, y))
                if column == 1:
                    surface.blit(self.tile_type[0], (x, y))
                    surface.blit(self.tile_type[1], (x, y))
                if column == 2:
                    surface.blit(self.tile_type[0], (x, y))
                    surface.blit(self.tile_type[2], (x, y))#this should be outer wall in place of 0/floor tile
                
                column_indx += 1
            row_indx += 1
            column_indx = 0

"""
0 is walkable
1 destructable wall but not walkable if wall there
    --> 0 nothing = 92%
    --> 1 is random gun 5% 
    --> 2 is power_up 3%
2 non destructible oute walls bullets can ricochet on them
6 is place for character

#####INNER ROOM######
(1)x-------------x(2)




(3)x-------------x(4)

(1): row = 1, column = 1
(2): row = 1, column = n-1
(3): row = n-1, column = 1
(4): row = n-1, column = n-1
"""