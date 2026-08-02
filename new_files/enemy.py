import pygame as pg
import character as char
import animation as anim

class enemy(char.Character):
    def __init__(self, pos, char_stat, hitbox_info, scale, last_update):#last_update is temporary
            super().__init__(pos, char_stat, hitbox_info, scale, last_update)
            