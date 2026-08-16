import pygame as pg
import math 
import collision_world as coll
import animation as anim
import collision_proj as coll_proj
import rotate_img as rimg
import convert_to_tiles as ctt

class Projectile:
    def __init__(self, proj_pos, proj, obj_pos, creation):
        if proj["type"] == "fire magic":
            self.image = anim.fireball
                
        if proj["type"] == "bullet":
            self.image = anim.kogel

        self.x, self.y = proj_pos[0], proj_pos[1]
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
    
    def update_proj_pos(self, world):
        projectile_collision = coll.Collision_world()
        x, y = (self.x + self.dir_x*self.speed), (self.y + self.dir_y*self.speed)
        if 0 < x < world.world_width and 0 < y < world.world_height:
            tile_xy = ctt.to_tiles((self.x + self.dir_x*self.speed), (self.y + self.dir_y*self.speed))
            if world.world_map[tile_xy[1], tile_xy[0]] in range(0, 2):
                self.x += self.dir_x*self.speed
                self.y += self.dir_y*self.speed
                return projectile_collision.is_allowed(world.world_map, (self.x, self.y), (self.dir_x*self.speed, self.dir_y*self.speed), self.proj_area)
        return True

    def rotate_projectile(self):
        rot_proj = rimg.Rotate()

    def collision_char(self, char_pos, char_hitbox):
        collision = coll_proj.Collision_proj()
        return collision.is_allowed((self.x, self.y), char_pos, self.proj_area, char_hitbox)

        
    def draw(self, screen, img, camera):
        if img is not None:
            screen.blit(img, (self.x - camera[0], self.y - camera[1]))