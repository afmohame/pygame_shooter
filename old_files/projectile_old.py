import pygame as pg
import math
import world_old

class Projectile():
    def __init__(self, proj_pos, proj_type, proj_area, damage, speed, life_time, spawn_time, player_pos):
        self.x, self.y = proj_pos[0], proj_pos[1]
        self.proj_type = proj_type
        self.proj_area = proj_area
        self.damage = damage
        self.speed = speed
        self.life_time = life_time
        self.spawn_time = spawn_time

        self.playerx, self.playery = player_pos[0], player_pos[1]
        dx, dy = player_pos[0] - self.x, player_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        #bcs if player and projectile have distance = 0 it will crash
        if distance == 0:
            self.dir_x = 0
            self.dir_y = 0
        else:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
    
    def collision(self, player, world_map):
        hitbox = {"left": player.x, "right": player.x + player.hitbox_width - 1, "top": player.y, "bottom": player.y + player.hitbox_height - 1}
        if (hitbox["left"] <= self.x <= hitbox["right"]) and (hitbox["top"] <= self.y <= hitbox["bottom"]):
            player.hp -= self.damage
            print(f"target hp: {player.hp}")
            return True
        
        if not world_map.move_allowed((self.x, self.y), (self.proj_area, self.proj_area)):
            return True
        
        else:
            return False
        
    def update(self):
        self.x += self.dir_x*self.speed
        self.y += self.dir_y*self.speed

    def draw_proj(self, surface, proj_image, camera):
        surface.blit(proj_image, (self.x - camera[0], self.y - camera[1]))
