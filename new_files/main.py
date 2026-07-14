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
weapons = weapon.Weapon((5, 5), cte.revolver, anim.revolver, (0,0)) #mouse pos in init is dumb
objects = [player, world_map, start_menu, weapon]
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def handling_events(events):
    for event in events:
        if event.type == pg.QUIT:
            return False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                return False
    return True

while run == True:
    clock.tick(cte.fps)
    screen.fill(0)
    events = pg.event.get()
    run = handling_events(events)
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
        pg.display.flip()

pg.quit()