import pygame as pg
import weapon
import cte
import world
import enemy
import player
import random
import animation as anim
import menu
import camera

pg.init()
screen = pg.display.set_mode((cte.screen_w, cte.screen_h))
clock = pg.time.Clock()
run, bool_start = True, True

last_update_main, last_spawn = pg.time.get_ticks(), pg.time.get_ticks()
anim_cooldown, spawn_cooldown = 100, 500
frame, bot1_frame = 0, 0
max_enemies = 13

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
player = player.Player(cte.pos, cte.player_info, cte.scale, cte.last_update_player, cte.tile_size[0], anim.player_animations["idle"])
bot = enemy.Enemy(cte.bot_pos, cte.bot1_info, cte.scale, cte.last_update_bot1, cte.last_atk_bot1, cte.tile_size[0], anim.bot1_animations["idle"])
world_map = world.World()
world_map.generate_world()
cam = camera.Camera(cte.camera_pos) 
start_menu = menu.Menu()
weapons = weapon.Weapon((5, 5), anim.revolver, cte.revolver, cte.pos) #mouse pos in init is dumb
objects = [world_map, player, weapons, bot]
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
draw_list = [world_map, player, weapons, bot]
ennemy_list = []
char_list = [player]

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

def remove_projectile(projectile_list):
    for proj in projectile_list.copy():
        remove_proj = False
        if world_map.world_map[int(proj.y//cte.tile_size[0]), int(proj.x//cte.tile_size[0])] not in range(2, 8): 
            proj.draw(screen, anim.kogel, cam.camera_pos) 
            #will have to go for testing 
        pg.draw.rect( screen, "blue", ( proj.x - cam.camera_pos[0], proj.y - cam.camera_pos[1], proj.proj_area[0], proj.proj_area[1] ), 2 ) #will have to go for testing

        if not proj.update_proj_pos(world_map):
            remove_proj = True

        # enemy bullet
        if projectile_list is cte.list_of_enemy_projectile:
            if proj.collision_char((player.x, player.y), (player.hitbox_width, player.hitbox_height)):
                player.take_damage(proj.damage)
                remove_proj = True

        # player bullet
        elif projectile_list is cte.list_of_player_projectile:
            for bot in ennemy_list:
                if proj.collision_char((bot.x, bot.y), (bot.hitbox_width, bot.hitbox_height)):
                    bot.take_damage(proj.damage)
                    remove_proj = True
                    break

        if pg.time.get_ticks() - proj.spawn_time >= proj.life_time:
            remove_proj = True

        if remove_proj:
            projectile_list.remove(proj)
            #the same idea for ennemy list

def spawn():
    global last_spawn 
    if len(ennemy_list) <= max_enemies:
        if now - last_spawn >= spawn_cooldown:
            last_spawn = now
            choose = random.randint(1, 3)
            if choose == 1:
                bot = enemy.Enemy(cte.bot_pos, cte.bot1_info, cte.scale, cte.last_update_bot1, cte.last_atk_bot1, cte.tile_size[0], anim.bot1_animations["idle"])
                bot.spawn_bot(world_map)
                ennemy_list.append(bot)
                print(f"the length of enemy list is: {len(ennemy_list)}")
            if choose == 2:
                pass
            if choose == 3:
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

        for i in ennemy_list:
            if i not in char_list:
                char_list.append(i)
        cam.update_camera(player.center, (cte.screen_w, cte.screen_h), cte.world_dim, cte.tile_size[0])
        world_map.draw(screen, cam.camera_pos)
        player.move(world_map)
        
        ### Bots ###
        spawn()
        ### Bots and player ###
        if now - last_update_main >= anim_cooldown:
            last_update_main = now
            for char in char_list.copy():
                char.frame += 1
                if char.frame >= len(char.current_anim):
                    char.frame = 0

        for char in char_list.copy():
            char.draw(screen, char.current_anim[char.frame], cam.camera_pos)
            char.update_tile_pos()
            char.update_center_char()
            if char.dead():
                if char is player:
                    run = False
                elif char in ennemy_list: #, bot2, bot3):
                    ennemy_list.remove(char)
                    char_list.remove(char)
            

        ### weapon ###
        weapons.update_mouse(pos_mouse, cam.camera_pos)
        weapons.rotate_gun(cte.orbit, player.center)
        weapons.draw(screen, weapons.gun_img, cam.camera_pos)
        if shoot:
            print("shoot him")
            weapons.shoot(pos_mouse, now, cam.camera_pos)

        remove_projectile(cte.list_of_player_projectile)
        remove_projectile(cte.list_of_enemy_projectile)

        #will have to go for testing

        # PLAYER HITBOX
        pg.draw.rect(
            screen,
            "green",
            (
                player.x - cam.camera_pos[0],
                player.y - cam.camera_pos[1],
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
                bot.x - cam.camera_pos[0],
                bot.y - cam.camera_pos[1],
                bot.hitbox_width,
                bot.hitbox_height
            ),
            2
        )
        #will have to go for testing
        pg.display.flip()

        

pg.quit()