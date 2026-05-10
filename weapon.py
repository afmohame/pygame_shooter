import pygame as pg
import projectile
import math
import cte


class Weapons():
    def __init__(self, weapon_xy, shooting_power, drop_rate, rarity, image, radius, ricochet, center_char, speed, bullet_img):
        self.x, self.y = weapon_xy[0], weapon_xy[1]
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.rarity = rarity
        self.image = image
        self.radius = radius
        self.ricochet = ricochet
        self.center_char = center_char #tuple (x, y)
        self.speed = speed
        self.bullet_img = bullet_img
    
    def update_mouse_pos(self, mouse_pos):
        self.mx, self.my = mouse_pos[0], mouse_pos[1]

    def rotate_gun(self, orbit_x, orbit_y, center_rot_char):
        #print(f"self.mx: {self.mx}, self.my: {self.my}")
        #print(f"center_rot_char[0]: {center_rot_char[0]}, center_rot_char[1]: {center_rot_char[1]}")

        dx, dy = self.mx - center_rot_char[0], self.my - center_rot_char[1]
        angle = math.degrees(math.atan2(dy, dx)) + 0 #0 is correction angle
        #print(f"dx: {dx}, dy: {dy}")
        
        #flips the image if left from character
        if dx < 0:
            base_image = pg.transform.flip(self.image, False, True)
        else:
            base_image = self.image
        self.gun_surf = pg.transform.rotate(base_image, -angle)

        rad = math.radians(angle)
        #descrives where the gun is relative to center character
        rot_offset_x = orbit_x*math.cos(rad) + orbit_y*math.sin(rad)
        rot_offset_y = orbit_x*math.sin(rad) + orbit_y*math.cos(rad)

        #where the gun is placed in the world
        self.gun_center_x = center_rot_char[0] + rot_offset_x
        self.gun_center_y = center_rot_char[1] + rot_offset_y
        
        self.rot_gun_screen = self.gun_surf.get_rect(center=(self.gun_center_x, self.gun_center_y))

    def shoot(self, current_time, mouse_click):
        proj = projectile.Projectile((self.gun_center_x, self.gun_center_y), "revolver bullet", cte.gun_info["area"], 
                                 cte.gun_info["damage"], cte.gun_info["speed"], cte.gun_info["life_time"],current_time,
                                 mouse_click)

        cte.list_of_player_projectile.append(proj)

    def draw_gun(self, screen, blit_image, pos, camera):
        screen.blit(blit_image, (pos[0] - camera[0], pos[1] - camera[1]))