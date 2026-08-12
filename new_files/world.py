import numpy as np #array[row, column] || column is vertical and row is horizontal
import cte
import pygame as pg
import collision_world as coll

class World:
    def __init__(self):
        self.world_width, self.world_height = cte.world_dim[0]*cte.tile_size[0], cte.world_dim[1]*cte.tile_size[0]
        self.tile_size = cte.tile_size[0]
        self.world_dim = cte.world_dim
        self.floor, self.destr_wall = cte.floor, cte.destr_wall
        self.outer_wall = {
            3: cte.outer_walls,
            4: pg.transform.rotate(cte.outer_walls, 90),
            5: pg.transform.rotate(cte.outer_walls, 180),
            6: pg.transform.rotate(cte.outer_walls, 270),
            7: self.destr_wall
        }
        self.tile_type = {
            1: self.floor, #walkable
            2 : self.destr_wall #not walkable
            }
        self.draw_tile = {0}
        self.world_map = np.full((self.world_dim[1], self.world_dim[0]), 1, dtype = int)
        self.coll = coll.Collision_world()
         
    def generate_world(self):
        self.world_map[1:-1, 0] = 3
        self.world_map[-1, 1:-1] = 4
        self.world_map[1:-1, -1] = 5
        self.world_map[0, 1:-1] = 6
        self.world_map[0, -1] = 7
        self.world_map[0, 0] = 7
        self.world_map[-1, 0] = 7
        self.world_map[-1, -1] = 7

        self.world_map[1:-1, 1:-1] = np.random.choice(
            [1, 2], #number(s) to randomly disperse in the room
            size = (self.world_dim[1] - 2, self.world_dim[0] - 2), #boundaries where to disperse them
            p = [0.87, 0.13] #probabilities of 0 and 1 respectively
        )
        self.world_map[1:4, 1:4] = 0 #where the player will spawn
        self.world_map[-4:-1, -4:-1] = 0 #where bots will spawn

        print(self.world_map)
    
    def is_walkable(self, current_position, speed, hitbox_wh):
        self.current_position = current_position
        advance = self.coll.is_allowed(self.world_map, current_position, speed, hitbox_wh)
        if not advance:
            return False
        if advance:
            return True
        

    def draw(self, surface, camera):
        row_indx, column_indx = 0, 0
        for row in self.world_map:
            for column in row:
                x = column_indx*self.tile_size - camera[0]
                y = row_indx*self.tile_size - camera[1]
                if column == 3:
                    surface.blit(self.tile_type[1], (x, y))
                    surface.blit(self.outer_wall[3], (x, y))
                if column == 4:
                    surface.blit(self.tile_type[1], (x, y))
                    surface.blit(self.outer_wall[4], (x, y))
                if column == 5:
                    surface.blit(self.tile_type[1], (x, y))
                    surface.blit(self.outer_wall[5], (x, y))
                if column == 6:
                    surface.blit(self.tile_type[1], (x, y))
                    surface.blit(self.outer_wall[6], (x, y))
                if column == 1 or column == 0:
                    surface.blit(self.tile_type[1], (x, y))
                if column in (2, 7):
                    surface.blit(self.tile_type[1], (x, y))
                    surface.blit(self.tile_type[2], (x, y))#this should be outer wall in place of 0/floor tile
                
                column_indx += 1
            row_indx += 1
            column_indx = 0
