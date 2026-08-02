import pygame as pg

class Collision:
    def __init__(self):
        pass

    def convert_pos_to_tile(self, pos, speed, tile_size, corner, hitbox = None):
        if hitbox is None:
            tile = (int((pos[0] + speed[0])//tile_size), int((pos[1] + speed[1])//tile_size))
        if corner == "tr":
            tile = (int((pos[0] + hitbox + speed[0])//tile_size), int((pos[1] + speed[1])//tile_size))
        if corner == "bl":
            tile = (int((pos[0] + speed[0])//tile_size), int((pos[1] + hitbox + speed[1])//tile_size))
        if corner == "br":
            tile = (int((pos[0] + hitbox[0] + speed[0])//tile_size), int((pos[1] + hitbox[1] + speed[1])//tile_size))
        return tile

    def is_allowed(self, world_map, current_position, speed, tile_size, hitbox_wh):
        hitbox_wh = (hitbox_wh[0] - 1, hitbox_wh[1] - 1)
        future_hitbox = {
            "tl": self.convert_pos_to_tile(current_position, speed, tile_size, "tl"), #top left
            "tr": self.convert_pos_to_tile(current_position, speed, tile_size, "tr", hitbox_wh[0]), #top right
            "bl": self.convert_pos_to_tile(current_position, speed, tile_size, "bl" ,hitbox_wh[1]), #bottom left
            "br": self.convert_pos_to_tile(current_position, speed, tile_size, "br" ,hitbox_wh) #bottom right
        }
        #topleft
        if world_map[future_hitbox["tl"][1], future_hitbox["tl"][0]] in range(2, 8):
            return False
        #topright
        if world_map[future_hitbox["tr"][1], future_hitbox["tr"][0]] in range(2, 8):
            return False
        #bottomleft
        if world_map[future_hitbox["bl"][1], future_hitbox["bl"][0]] in range(2, 8):
            return False
        #bottomright
        if world_map[future_hitbox["br"][1], future_hitbox["br"][0]] in range(2, 8):
            return False
        
        return True


