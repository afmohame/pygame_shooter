import pygame as pg
import numpy as np
import math

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
            p = [0.87, 0.13] #probabilities of 0 and 1 respectively
        )
        self.world_map[1:4, 1:4] = 0 #where the player will spawn
        self.world_map[-5:-2, -5:-2] = 0 #where bots will spawn

    def get_world(self):
        return self.world_map
    
    def place_char(self):
        pass

    def move_allowed(self, char_pos, char_hitbox):#modulo geeft rest -> niet gebruiken
        hitbox = {"left": char_pos[0], "right": char_pos[0] + char_hitbox[0] - 1, "top": char_pos[1], "bottom": char_pos[1] + char_hitbox[1] - 1}
        #TOP LEFT
        tile_x = int((hitbox["left"])//self.tile_size) #gives which tile I am on
        tile_y = int((hitbox["top"])//self.tile_size) #gives which tile I am on
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #TOP RIGHT
        tile_x = int((hitbox["right"])//self.tile_size)
        tile_y = int((hitbox["top"])//self.tile_size)
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #BOTTOM LEFT
        tile_x = int((hitbox["left"])//self.tile_size)
        tile_y = int((hitbox["bottom"])//self.tile_size)
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        #BOTTOM RIGHT
        tile_x = int((hitbox["right"])//self.tile_size)
        tile_y = int((hitbox["bottom"])//self.tile_size)
        if self.world_map[tile_y, tile_x] != 0:
            return False
        
        return True

    def is_walkable_neighbors(self, tile_pos):
        self.list_walk_dir = []
        neighbour_tiles = {"up": (tile_pos[0], tile_pos[1] - 1), "down": (tile_pos[0], tile_pos[1] + 1),
                           "left": (tile_pos[0] - 1, tile_pos[1]), "right": (tile_pos[0] + 1, tile_pos[1])}
        
        for key, value in neighbour_tiles.items():
            x, y = value

            if 0 <= x < self.world_width - 1 and 0 <= y < self.world_height - 1:#checks if neighboring tile is in world borders
                if self.world_map[y, x] == 0:
                    self.list_walk_dir.append(value)

        return self.list_walk_dir

    def find_path(self, start_tile, goal_tile):#t(n) = g(n) + h(n)
        curr_pos = start_tile 
        not_checked = [] #tiles not checked
        checked = [] #tiles checked
        g_cost = 0 #how far from start
        #Manhattan distance -> moves in up, down, left, right so difference of coordinates
        h_cost = abs(curr_pos[0] - goal_tile[0]) + abs(curr_pos[1] - goal_tile[1]) #distance current tile to goal/player tile
        t_cost = g_cost + h_cost
        parent = None

        not_checked.append([start_tile, (g_cost, h_cost, t_cost), parent])

        curr_record = not_checked[0]      # full tile data first index
        curr_tile = curr_record[0]        # only the tile position

        neighbor = self.is_walkable_neighbors(curr_tile)

        checked.append(curr_record)       # add full tile data to checked
        not_checked.remove(curr_record)   # remove only this tile from not_checked

        for i in neighbor:
            h_neighbor = abs(i[0] - goal_tile[0]) + abs(i[1] - goal_tile[1])
            g_neighbor = curr_record[1][0] + 1
            t_neighbor = g_neighbor + h_neighbor
            parent_neighbor = curr_record[0]
            
            present_in_not_checked = False
            present_in_checked = False

            for tile in not_checked:
                if tile[0] == i:
                    present_in_not_checked = True      
            for tile2 in checked:
                if tile2[0] == i:
                    present_in_checked = True

            if not present_in_checked and not present_in_not_checked:
                not_checked.append([i, (g_neighbor, h_neighbor, t_neighbor), parent_neighbor])

        goal = False
        goal_record = None
        while not_checked and not goal:
            best_record = not_checked[0]
            best_cost = not_checked[0][1][2]
            best_tile = not_checked[0][0]

            for i in not_checked:
                if best_cost > i[1][2]:
                    best_cost = i[1][2]
                    best_tile = i[0]
                    best_record = i
            
            curr_record = best_record
            curr_tile = curr_record[0]

            not_checked.remove(curr_record)
            checked.append(curr_record)
            if not curr_record[0] == goal_tile:
                neighbor = self.is_walkable_neighbors(curr_tile)
                for i in neighbor:
                    h_neighbor = abs(i[0] - goal_tile[0]) + abs(i[1] - goal_tile[1])
                    g_neighbor = curr_record[1][0] + 1
                    t_neighbor = g_neighbor + h_neighbor
                    parent_neighbor = curr_record[0]
                    
                    present_in_not_checked = False
                    present_in_checked = False

                    for tile in not_checked:
                        if tile[0] == i:
                            present_in_not_checked = True      
                    for tile2 in checked:
                        if tile2[0] == i:
                            present_in_checked = True

                    if not present_in_checked and not present_in_not_checked:
                        not_checked.append([i, (g_neighbor, h_neighbor, t_neighbor), parent_neighbor])
            else:
                goal = True
                goal_record = curr_record

        if goal_record == None:
            return []
        
        path_retrace = []
        path_retrace.append(goal_record[0])
        parent_retrace = goal_record[2]
        while parent_retrace != None:
            for i in checked:
                if i[0] == parent_retrace:
                    path_retrace.append(i[0])
                    parent_retrace = i[2]
                    break

        path_retrace.reverse()  
        return path_retrace 
        
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