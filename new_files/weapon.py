import pygame as pg
import animation as anim
import math 
import projectile as proj

class Weapon(proj.Projectile):
    def __init__(self, pos, img, gun, char_pos): #adding drop_rate, rarity, radius, ricochet,
        proj_pos = (pos[0] + gun["sprite_w_h"][0]//2, pos[1] + gun["sprite_w_h"][1]//2)
        super().__init__(proj_pos, gun["projectile"], char_pos)
        self.x, self.y = pos[0], pos[1]
        self.mx, self.my = 0, 0
        self.img = img

    def update_mouse(self, pos):
        self.mx, self.my = pos[0], pos[1]
    
    def rotate_gun(self, orbit, center_char):
        dx, dy = self.mx - center_char[0], self.my - center_char[1]
        angle = math.degrees(math.atan2(dy, dx)) #calc the angle from center char to mouse position

        #flipping the image if left or right from character
        if dx < 0:
            base_image = pg.transform.flip(self.img, False, True)#self.img, spiegel x-as, spiegel y-as
        else:
            base_image = self.img
        self.gun_img = pg.transform.rotate(base_image, -angle)

        #where the gun is with respect to the mouse position on a fixed radius
        rad = math.radians(angle)
        rott_offset_x = orbit[0]*math.cos(rad) - orbit[1]*math.sin(rad)
        rott_offset_y =  orbit[0]*math.sin(rad) + orbit[1]*math.cos(rad)

        gun_center = (center_char[0] + rott_offset_x, center_char[1] + rott_offset_y)

        self.rot_gun_screen = self.gun_img.get_rect(center=gun_center)

    def shoot(self, img):
        pass


    def draw_weapon(self, surface, img, position, camera = None):#moet draw zijn niet draw_weapon
        surface.blit(img, (position[0], position[1]))