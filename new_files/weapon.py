import pygame as pg
import animation as anim
import math 
import projectile as proj
import cte 
import rotate_img as rimg

class Weapon():
    def __init__(self, pos, img, gun, char_pos): #adding drop_rate, rarity, radius, ricochet,
        self.x, self.y = pos[0], pos[1] #position of what?
        self.mx, self.my = 0, 0
        self.img = img
        self.gun = gun
        self.gun_center = pos

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

        self.gun_center = (center_char[0] + rott_offset_x, center_char[1] + rott_offset_y)

        self.rot_gun_screen = self.gun_img.get_rect(center=self.gun_center)
        #self.rotated_gun = rimg.rotate_image(self.gun_img, angle, orbit, center_char)
        #might be implemented later
        
    def shoot(self, mouse_pos, time):
            new_projectile = proj.Projectile(self.gun_center, self.gun['projectile'], mouse_pos, time)
            cte.list_of_player_projectile.append(new_projectile)

    def draw(self, surface, img, position, camera = None):#moet draw zijn niet draw_weapon
        surface.blit(img, (position[0], position[1]))