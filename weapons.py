import pygame as pg
import math
#import main
screen = pg.display.set_mode((800, 800))
clock = pg.time.Clock()

class Weapons():
    def __init__(self, x, y, shooting_power, drop_rate, rarity, image, radius, ricochet, center_char, bullet_count = None):
        self.x, self.y = x, y
        self.shooting_power = shooting_power
        self.drop_rate = drop_rate
        self.rarity = rarity
        self.image = image
        self.radius = radius
        self.ricochet = ricochet
        self.center_char = center_char #tuple (x, y)
        self.bullet_count = bullet_count
    
    def Rotate_gun(self, mx, my, angle):
        self.mx = mx
        self.my = my
        self.angle = angle

    def Shoot(self, shoot):
        if shoot:
            pass

sprite_revolver = pg.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
radius, orbit_rad, center_rot_x, center_rot_y = 10, 50, 400, 400
width, height = 80, 120
center_charx, center_chary = center_rot_x, center_rot_y
weapon_x, weapon_y = 50, 60
revolver = Weapons(weapon_x, weapon_y, 3, 10, "common", sprite_revolver, radius, 2, (center_charx, center_chary))

anchor_surface = pg.Surface((radius, radius), pg.SRCALPHA)
anchor_point = pg.draw.circle(anchor_surface, (0, 0, 200), (radius/2, radius/2), radius/2)

#char making
surface_char = pg.Surface((width, height), pg.SRCALPHA)
char_rect = pg.draw.rect(surface_char, (200, 0, 0), (0, 0, width, height))

angle, corr_angle = 0, 0
run = True
while run:
    screen.fill((0, 0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    mx, my = pg.mouse.get_pos()
    dx, dy = mx - center_rot_x, my - center_rot_y
    angle = math.degrees(math.atan2(dy, dx))-corr_angle

    gun_rect = pg.transform.rotate(revolver.image, -angle)

    offset_x, offset_y = orbit_rad, 0

    rad = math.radians(angle)
    rot_offset_x = offset_x*math.cos(rad) - offset_y*math.sin(rad)
    rot_offset_y = offset_x*math.sin(rad) + offset_y*math.cos(rad)
    
    gun_center_x = center_rot_x + rot_offset_x
    gun_center_y = center_rot_y + rot_offset_y

    rot_gun_screen = gun_rect.get_rect(center=(gun_center_x, gun_center_y))

    #character hitbox
    screen.blit(surface_char, (center_charx - width//2, center_chary - height//2))
    screen.blit(anchor_surface, (center_charx-radius/2, center_chary-radius/2))
    screen.blit(gun_rect, rot_gun_screen)

    pg.display.update()
    clock.tick(60)
pg.quit()