import pygame as pg
import math

pg.init()
screen = pg.display.set_mode((800, 800))
clock = pg.time.Clock()
run = True
angle = 0
centerx, centery = 400, 400
dx, dy = 400, 400
width, height = 100, 40
top_left = (dx, dy)
top_right = (dx+width, dy)
bottom_left = (dx, dy+height)
botom_right = (dx+width, dy+height)
anchor_mouse = (dx, dy+height)
d_angle = 0
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    if event.type == pg.MOUSEMOTION:
        mx, my = pg.mouse.get_pos()
        #print(dx)
        #print(dy)


    player_pos = screen.get_rect().center
    pg.draw.rect(screen, (200, 0, 0), (player_pos[0], player_pos[1], width, height))
    pg.draw.circle(screen, (0, 200, 0), anchor_mouse, 5)


    pg.display.flip()
    pg.display.update()
    clock.tick(60)
pg.quit()