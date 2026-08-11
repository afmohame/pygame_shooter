import pygame as pg
import convert_to_tiles as ctt


class Collision_world:
    def __init__(self):
        pass

    def is_allowed(self, world_map, current_position, speed, hitbox_wh):
        hitbox_wh = (hitbox_wh[0] - 1, hitbox_wh[1] - 1)
        future_hitbox = {
            "tl": ctt.to_tiles((current_position[0] + speed[0]), (current_position[1] + speed[1])), #top left
            "tr": ctt.to_tiles((current_position[0] + speed[0] + hitbox_wh[0]), (current_position[1] + speed[1])), #top right
            "bl": ctt.to_tiles((current_position[0] + speed[0]), (current_position[1] + hitbox_wh[1] + speed[1])), #bottom left
            "br": ctt.to_tiles((current_position[0] + hitbox_wh[0] + speed[0]), (current_position[1] + hitbox_wh[1] + speed[1])), #bottom right
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