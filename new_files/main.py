import pygame as pg
import weapon
import character
import cte
import world
import enemy
import projectile
import player
import random
import math
import animation as anim
import menu

pg.init()
screen = pg.display.set_mode((cte.screen_w, cte.screen_h))
clock = pg.time.Clock()
run, bool_start = True, True

last_update_main = pg.time.get_ticks()
anim_cooldown = 100
frame = 0

current_animation = anim.player_animations["run_Rside"]

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
player = player.Player(cte.pos, cte.char_stat, cte.hitbox_info, cte.scale, cte.last_update_player, cte.tile_size)
world_map = world.World()
world_map.generate_world()
start_menu = menu.Menu()
weapons = weapon.Weapon((5, 5), anim.revolver, cte.revolver, cte.pos) #mouse pos in init is dumb
objects = [player, world_map, start_menu, weapon]
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def handling_events(events):
    run = True
    shoot = False

    for event in events:
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
        if event.type == pg.MOUSEBUTTONDOWN and start_menu.start == True:
            if event.button == 1:
                shoot = True
    return run, shoot

while run == True:
    clock.tick(cte.fps)
    screen.fill(0)
    events = pg.event.get()
    run, shoot = handling_events(events)
    pos_mouse = pg.mouse.get_pos()

    if start_menu.start == None:
        start_menu.show_menu("start", screen, events)
    
    if start_menu.start == False:
        run = False

    if start_menu.start == True:
        now = pg.time.get_ticks()
        if now - last_update_main >= anim_cooldown:
            last_update_main = now
            frame += 1
            if frame >= len(current_animation):
                frame = 0

        #player.update_tile_pos()
        player.move(world_map)
        world_map.draw_world(screen)
        player.draw_char(screen, player.current_anim[frame], player.x, player.y, (0, 0))

        ### weapon ###
        weapons.update_mouse(pos_mouse)
        weapons.rotate_gun(cte.orbit, player.center_char((player.x, player.y)))
        weapons.draw_weapon(screen, weapons.gun_img, weapons.rot_gun_screen)

        if shoot:
            print("shoot him")
            weapons.shoot(pos_mouse, now)
        
        for proj in cte.list_of_player_projectile.copy():
            proj.update_proj_pos()
            proj.draw_proj(screen, anim.fireball)

            now = pg.time.get_ticks()
            if now - proj.spawn_time >= proj.life_time:
                cte.list_of_player_projectile.remove(proj)

        pg.display.flip()

pg.quit()