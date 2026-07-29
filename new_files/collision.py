import pygame as pg

class Collision:
    def __init__(self):
        pass
    
    def is_allowed(self, world_map, current_position, speed, tile_size, hitbox_wh):
        current_tile_pos = (int(current_position[0]//tile_size), int(current_position[1]//tile_size))
        future_tile_pos =  (int((current_position[0] + speed[0])//tile_size), int((current_position[1] + speed[1])//tile_size))
        current_hitbox = {
            "tl": (current_position[0], current_position[1]), #top left
            "tr": (current_position[0] + hitbox_wh[0], current_position[1]), #top right
            "bl": (current_position[0], current_position[1] + hitbox_wh[1]), #bottom left
            "br": (current_position[0] + hitbox_wh[0], current_position[1] + hitbox_wh[1]) #bottom right
        }
        
        if world_map[future_tile_pos[1], future_tile_pos[0]] == 0:
            return True
        else:
            return False
        if move in ("WA", "WD", "SA", "SD"):
            if move == "WA":
                next_tile_pos = ((current_position[0] - speed)//tile_size, (current_position[1] - speed)//tile_size)

        if move in ("W", "S", "A", "D"):
            if move == "W":
                next_tile_pos = ((current_position[0] + speed)//tile_size, (current_position[1] + speed)//tile_size)


