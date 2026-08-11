import math
import pygame as pg

def rotate_image(img, angle, orbit, center_char, pos = None):
    #flipping the image if left or right from character
    if pos[0] < 0:
        base_image = pg.transform.flip(img, False, True)#self.img, spiegel x-as, spiegel y-as
    else:
        base_image = img
    gun_img = pg.transform.rotate(base_image, -angle)

    rad = math.radians(angle)
    rad = math.radians(angle)
    rott_offset_x = orbit[0]*math.cos(rad) - orbit[1]*math.sin(rad)
    rott_offset_y =  orbit[0]*math.sin(rad) + orbit[1]*math.cos(rad)

    gun_center = (center_char[0] + rott_offset_x, center_char[1] + rott_offset_y)

    return img.get_rect(center=gun_center)
    