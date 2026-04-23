import pygame as pg
import math

pg.init()
screen = pg.display.set_mode((800, 800))
clock = pg.time.Clock()
run = True

dx, dy = 400, 400
width, height = 100, 40
anchor_mouse = (dx, dy)#this is the point where mouse point to
d_angle = 0
radius, orbit_rad = 3, 150
#pg.SRCALPHA laat toe om transparante pizels te hebben.
rect_surface = pg.Surface((width, height), pg.SRCALPHA)
rect_screen = pg.draw.rect(rect_surface, (209, 0, 0), (0, 0, width, height))

anchor_surface = pg.Surface((2*radius, 2*radius), pg.SRCALPHA)
anchor_point = pg.draw.circle(anchor_surface, (0, 0, 200), (radius, radius), radius)
angle = 0
while run:
    screen.fill((0,0,0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    mx, my = pg.mouse.get_pos()
    dx, dy = mx - anchor_mouse[0], -(my - anchor_mouse[1])
    angle = math.degrees(math.atan2(dy, dx))-d_angle

    rot_rect = pg.transform.rotate(rect_surface, -angle)

    offset_x, offset_y = orbit_rad, 0
    
    rad = math.radians(angle)
    rot_offset_x = offset_x*math.cos(rad) - offset_y*math.sin(rad)
    rot_offset_y = offset_x*math.sin(rad) + offset_y*math.cos(rad)
    
    rect_center_x = anchor_mouse[0] + rot_offset_x
    rect_center_y = anchor_mouse[1] + rot_offset_y

    rot_rect_screen = rot_rect.get_rect(center=(rect_center_x, rect_center_y))

    screen.blit(rot_rect, rot_rect_screen)
    screen.blit(anchor_surface, (anchor_mouse[0] - radius, anchor_mouse[1] - radius))

    pg.display.update()
    clock.tick(60)
pg.quit()