import pygame as pg
import weapon
import characters
import cte
import world
import enemy
import projectile
import player
import random
import math
import cached_anim as ca

pg.init()
screen = pg.display.set_mode((cte.screen_w, cte.screen_h))
clock = pg.time.Clock()

last_update_main = pg.time.get_ticks()
anim_cooldown = 100
frame = 0

current_animation = ca.player_animations["run_Rside"]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
player = player.Player(cte.pos, cte.char_stat, cte.hitbox_info, cte.tile_size, cte.scale, cte.last_update_player)
world_map = world.World(cte.world_dim, cte.floor, cte.destr_wall, cte.outer_walls, cte.tile_size[0])
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

run = True
while run:
    clock.tick(cte.fps)
    screen.fill(0)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
    
    now = pg.time.get_ticks()
    if now - last_update_main >= anim_cooldown:
        last_update_main = now
        frame += 1
        if frame >= len(current_animation):
            frame = 0

    world_map.draw_world(screen)
    screen.blit(current_animation[frame], (300, 300))
    pg.display.flip()
pg.quit()