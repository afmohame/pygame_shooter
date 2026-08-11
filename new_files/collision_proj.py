import pygame as pg

#To make collision between projectile and characters
class Collision_proj:
    def __init__(self):
        pass

    def is_allowed(self, proj_pos, char_pos, hitbox_proj, hitbox_char):
        projectile = {
            "tl": (proj_pos[0], proj_pos[1]),
            "br": (proj_pos[0] + hitbox_proj[0], proj_pos[1] + hitbox_proj[1])
        }

        char = {
            "tl": (char_pos[0], char_pos[1]),
            "br": (char_pos[0] + hitbox_char[0], char_pos[1] + hitbox_char[1])
        }

        collision = ( projectile["tl"][0] < char["br"][0]
                      and projectile["br"][0] > char["tl"][0]
                      and projectile["tl"][1] < char["br"][1]
                      and projectile["br"][1] > char["tl"][1]
        )
        return collision