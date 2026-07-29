import pygame as pg
import math 

class Projectile:
    def __init__(self, proj_pos, proj, obj_pos, creation):
        self.x, self.y = proj_pos[0], proj_pos[1]
        self.proj_type = proj["type"]
        self.proj_area = proj["area"]#beter naam zoeken, maar dit is eigenlijk de hitbox ervan
        self.damage = proj["damage"]
        self.speed = proj["speed"]
        self.life_time = proj["life_time"]
        self.spawn_time = creation
        self.obj_pos = obj_pos

        dx, dy = self.obj_pos[0] - self.x, self.obj_pos[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        #otherwise, if the distance between projectile and char is 0, it will crash
        if distance == 0:
            self.dir_x = 0
            self.dir_y = 0
        else:
            self.dir_x = dx/distance
            self.dir_y = dy/distance
    
    def update_proj_pos(self):
        self.x += self.dir_x*self.speed
        self.y += self.dir_y*self.speed

    def collision(self, enemy):
        pass

    def draw_proj(self, screen, img, camera = None):
        screen.blit(img, (self.x, self.y))