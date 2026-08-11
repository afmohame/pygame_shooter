import pygame as pg
import weapon
import collision_proj as coll_proj
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
frame, bot1_frame = 0, 0

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
player = player.Player(cte.pos, cte.player_info, cte.scale, cte.last_update_player, cte.tile_size)
bot1 = enemy.Enemy(cte.bot_pos, cte.bot1_info, cte.scale, cte.last_update_bot1, cte.last_atk_bot1, cte.tile_size[0], anim.bot1_animations["idle"])
world_map = world.World()
world_map.generate_world()
start_menu = menu.Menu()
weapons = weapon.Weapon((5, 5), anim.revolver, cte.revolver, cte.pos) #mouse pos in init is dumb
objects = [world_map, player, weapon, bot1]
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
                #if world_map.world_map[int(pos_mouse[1]//cte.tile_size[0]), int(pos_mouse[0]//cte.tile_size[0])] not in range(2, 8):
                shoot = True
    return run, shoot

def remove_projectile(projectile_list, char_pos, char_hitbox):
    for proj in projectile_list.copy():
                remove_proj = False
                if world_map.world_map[int(proj.y//cte.tile_size[0]), int(proj.x//cte.tile_size[0])] not in range(2, 8):
                    proj.draw(screen, anim.kogel)
                #will have to go for testing
                pg.draw.rect(
                screen,
                "blue",
                (
                    proj.x,
                    proj.y,
                    proj.proj_area[0],
                    proj.proj_area[1]
                ),
                2
                )
                #will have to go for testing


                if not proj.update_proj_pos(world_map):
                    remove_proj = True
    
                if proj.collision_char(char_pos, char_hitbox):
                    remove_proj = True
    
                now = pg.time.get_ticks()
                if now - proj.spawn_time >= proj.life_time:
                    remove_proj = True
    
                if remove_proj:
                    projectile_list.remove(proj)
            #the same idea for ennemy list

def random_spawn():
    pass

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
            bot1_frame += 1
            if frame >= len(player.current_anim):
                frame = 0
            if bot1_frame >= len(bot1.current_anim):
                bot1_frame = 0
            

        #player.update_tile_pos()
        player.move(world_map)
        world_map.draw(screen)
        player.draw(screen, player.current_anim[frame], player.x, player.y, (0, 0))

        ### Bots ###
        bot1.draw(screen, bot1.current_anim[bot1_frame], bot1.x, bot1.y, (0, 0))

        ### weapon ###
        weapons.update_mouse(pos_mouse)
        weapons.rotate_gun(cte.orbit, player.center_char((player.x, player.y)))
        weapons.draw(screen, weapons.gun_img, weapons.rot_gun_screen)
        #weapons.draw(screen, weapons.gun_img, weapons.rotated_gun)

        if shoot:
            print("shoot him")
            weapons.shoot(pos_mouse, now)

        remove_projectile(cte.list_of_player_projectile, (bot1.x, bot1.y), (bot1.hitbox_width, bot1.hitbox_height))
        remove_projectile(cte.list_of_enemy_projectile, (player.x, player.y), (player.hitbox_width, player.hitbox_height))

        #will have to go for testing
        # PLAYER HITBOX
        pg.draw.rect(
            screen,
            "green",
            (
                player.x,
                player.y,
                player.hitbox_width,
                player.hitbox_height
            ),
            2
        )

        # BOT HITBOX
        pg.draw.rect(
            screen,
            "red",
            (
                bot1.x,
                bot1.y,
                bot1.hitbox_width,
                bot1.hitbox_height
            ),
            2
        )
        #will have to go for testing

        pg.display.flip()

        

pg.quit()