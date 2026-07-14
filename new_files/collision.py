import pygame as pg

class Collision:
    def __init__(self):
        pass
    
    def is_allowed(self, world_map, current_position, speed, tile_size, move):
        current_tile_pos = (current_position[0]//tile_size, current_position[1]//tile_size)
        return True
        if move in ("WA", "WD", "SA", "SD"):
            if move == "WA":
                next_tile_pos = ((current_position[0] - speed)//tile_size, (current_position[1] - speed)//tile_size)

        if move in ("W", "S", "A", "D"):
            if move == "W":
                next_tile_pos = ((current_position[0] + speed)//tile_size, (current_position[1] + speed)//tile_size)


