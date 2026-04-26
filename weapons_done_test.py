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
    
    def update_mouse_pos(self, mouse_pos):
        self.mx, self.my = mouse_pos[0], mouse_pos[1]

    def Rotate_gun(self, angle, offset_x, offset_y, center_rot_x, center_rot_y):
        self.gun_surf = pg.transform.rotate(self.image, -angle)

        rad = math.radians(angle)
        rot_offset_x = offset_x*math.cos(rad) - offset_y*math.sin(rad)
        rot_offset_y = offset_x*math.sin(rad) + offset_y*math.cos(rad)

        self.gun_center_x = center_rot_x + rot_offset_x
        self.gun_center_y = center_rot_y + rot_offset_y
        
        self.rot_gun_screen = self.gun_surf.get_rect(center=(self.gun_center_x, self.gun_center_y))

    def Shoot(self, shoot):
        if shoot:
            pass

sprite_revolver = pg.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
radius, orbit_rad, center_x, center_y = 10, 50, 400, 400
width, height = 80, 120
weapon_x, weapon_y = 50, 60
revolver = Weapons(weapon_x, weapon_y, 3, 10, "common", sprite_revolver, radius, 2, (center_x, center_y))

anchor_surface = pg.Surface((radius, radius), pg.SRCALPHA)
anchor_point = pg.draw.circle(anchor_surface, (0, 0, 200), (radius/2, radius/2), radius/2)

#char making
surface_char = pg.Surface((width, height), pg.SRCALPHA)
char_rect = pg.draw.rect(surface_char, (200, 0, 0), (0, 0, width, height))

angle, corr_angle = 0, 0
run = True
while run:
    screen.fill((100, 100, 100))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    revolver.update_mouse_pos(pg.mouse.get_pos())
    dx, dy = revolver.mx - center_x, revolver.my - center_y
    angle = math.degrees(math.atan2(dy, dx))-corr_angle
    
    revolver.Rotate_gun(angle, orbit_rad, 0, center_x, center_y)

    rot_gun_screen = revolver.rot_gun_screen

    #character hitbox
    screen.blit(surface_char, (center_x - width//2, center_y - height//2))
    screen.blit(anchor_surface, (center_x-radius/2, center_y-radius/2))
    screen.blit(revolver.gun_surf, rot_gun_screen)

    pg.display.update()
    clock.tick(60)
pg.quit()