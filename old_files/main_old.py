import pygame
import weapon_old 
import characters_old
import cte_old
import world_old
import enemy_old
import projectile_old
import player_old
import random
import math
pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
          
class Camera():
    def __init__(self, camera_xy):
        self.camera_x, self.camera_y = camera_xy[0], camera_xy[1]
        self.camera_xy = (self.camera_x, self.camera_y)
    
    def update_camera(self, screen, char_pos, sprite_w_h, world_dim, tile_size):#world_dim is in tiles not pixels
        camera_x_min, camera_x_max = 0, world_dim[0]*tile_size - screen[0]
        camera_y_min, camera_y_max = 0, world_dim[1]*tile_size - screen[1]

        center_char = (char_pos[0] + sprite_w_h[0]//2, char_pos[1] + sprite_w_h[1]//2)

        target_x = center_char[0] - screen[0]//2
        target_y = center_char[1] - screen[1]//2

        #clamp camera inside
        camera_x_min, camera_y_min = 0, 0
        camera_x_max =  max(0, world_dim[0]*tile_size - screen[0])
        camera_y_max = max(0, world_dim[1]*tile_size - screen[1])

        self.camera_x = max(camera_x_min, min(target_x, camera_x_max))
        self.camera_y = max(camera_y_min, min(target_y, camera_y_max))
        
        self.camera_xy = (self.camera_x, self.camera_y)

def spawn_bot(world_map, player):
    spawn_found = False
    attempts = 0

    while not spawn_found and attempts < 100:
        tile_x = random.randint(1, world_map.world_width - 2)
        tile_y = random.randint(1, world_map.world_height - 2)

        #checks if chosen tile is floor/walkable
        if world_map.world_map[tile_y, tile_x] == 0:

            spawn_x = tile_x * cte_old.tile_size[0]
            spawn_y = tile_y * cte_old.tile_size[0]

            dx = spawn_x - player.x
            dy = spawn_y - player.y
            distance = math.sqrt(dx**2 + dy**2)

            #don't spawn too close to player
            if distance > 500:
                new_bot = enemy_old.Enemy((spawn_x, spawn_y), cte_old.bot1_stats, cte_old.bot1_hitbox_info, cte_old.bot1_sprite_info,
                    sprite_bot1, cte_old.bot1_animation_info, cte_old.animation_moves_enemies, cte_old.frame, cte_old.last_update_bot1,
                    cte_old.last_atk, cte_old.tile_size[0])

                cte_old.list_of_enemies.append(new_bot)
                spawn_found = True

        attempts += 1

# screen
clock = pygame.time.Clock()

#sprites
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/revolver.png").convert_alpha() 
bullet_rev = pygame.image.load("sprites/images_chosen_for_game/bullet1.png").convert_alpha() 
sprite_bot1 = pygame.image.load("sprites/images_chosen_for_game/bot1_walking.png").convert_alpha()

# player
player1 = player_old.Player(
    cte_old.pos, cte_old.char_stat, cte_old.hitbox_info, cte_old.sprite_info, sprite_player, cte_old.animation_info, cte_old.animation_moves_player, 
    cte_old.frame, cte_old.last_update_player, cte_old.tile_size[0], (None, None))

#enemy 
bot1 = enemy_old.Enemy(
    (100, 100), cte_old.bot1_stats, cte_old.bot1_hitbox_info, cte_old.bot1_sprite_info, sprite_bot1, cte_old.bot1_animation_info, cte_old.animation_moves_enemies,
    cte_old.frame, cte_old.last_update_bot1, cte_old.last_atk, cte_old.tile_size[0])

#gun
weapon_xy = (cte_old.sprite_info["sprite_player_width"]*cte_old.scale, cte_old.scale*cte_old.sprite_info["sprite_player_height"]/2)
artillery = {"revolver": weapon_old.Weapons(weapon_xy, 3, 10, "common", sprite_revolver, cte_old.radius, 2, cte_old.center, cte_old.revolver_speed, bullet_rev)}

#world
floor = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/06_Dungeon_Tileset.png"), cte_old.tile_size)
outer_walls = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/00_right_outer_wall.png"), cte_old.tile_size)
destr_wall = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/column_sprite.png"), cte_old.tile_size)
world_map = world_old.World(cte_old.world_dim, floor, destr_wall, outer_walls, cte_old.tile_size[0])
world_map.generate_world()

#camera
camera_move = Camera(cte_old.camera_pos)
#animation preload
#-----------------------------------------------s
#                MAIN GAME LOOP
#-----------------------------------------------
cte_old.list_of_players.append(player1)
cte_old.list_of_guns.append(artillery["revolver"])
cte_old.list_of_enemies.append(bot1)
run = True

shoot = False
map_generate = True
last_bot_spawn = pygame.time.get_ticks()
bot_spawn_cooldown = 3000 #ms
while run:
    cte_old.screen.fill(cte_old.bg) #can't be deleted it refreshes the screen.

    #this block needs to be above other event.type otherwise it does not work 
    #repeating for event in pygame.event.get() is also not good
    #for loop does not create a local variable!!
    mouse_clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True


    pos_mouse = pygame.mouse.get_pos()
    #update animation
    current_time = pygame.time.get_ticks()#for animation tracks time passed
    
    #spawn bot1
    if current_time - last_bot_spawn >= bot_spawn_cooldown:
        spawn_bot(world_map, player1)
        last_bot_spawn = current_time
    #PLAYER
    for character in cte_old.list_of_players:
        character.moving(world_map)
        #camera
        camera_move.update_camera((cte_old.screen_w, cte_old.screen_h), (character.x, character.y), cte_old.sprite_w_h, cte_old.world_dim, cte_old.tile_size[0])
        #draw world
        world_map.draw_world(cte_old.screen, (camera_move.camera_x, camera_move.camera_y))

        #character.draw_hitbox(cte_old.screen, camera_move.camera_xy)#draws a hitbox in red
        character.make_animation(cte_old.black, cte_old.first_x, cte_old.first_y, cte_old.x_space, cte_old.y_space, cte_old.column_length)
        character.get_frame(current_time, cte_old.animation_cooldown)
        character.draw_char(cte_old.screen, character.get_animation(), character.x, character.y, camera_move.camera_xy)#puts character on screen which is a surface
        center_char_real = (character.x + cte_old.sprite_info["sprite_player_width"]*cte_old.scale/2, 
                       character.y + cte_old.scale*cte_old.sprite_info["sprite_player_height"]/2)
    
    #enemy
    for bot in cte_old.list_of_enemies.copy():
        bot.update(character, world_map, current_time)
        if not character.alive():
            run = False
        bot.make_animation(cte_old.black, cte_old.bot1_fx, cte_old.bot1_fy, cte_old.bot1_x_space, cte_old.bot1_y_space, cte_old.bot1_column_length)
        bot.get_frame(current_time, cte_old.animation_cooldown)
        #bot.draw_hitbox(cte_old.screen, camera_move.camera_xy)
        bot.draw_bot(cte_old.screen, bot.get_animation(), bot.x, bot.y, camera_move.camera_xy)
        #print(f"bot tile pos: {bot.tile_pos}")
    
    #enemy projectiles
    for proj in cte_old.list_of_enemy_projectile.copy():
        proj.update()
        proj.draw_proj(cte_old.screen, enemy_old.projectile_img, camera_move.camera_xy)

        if current_time - proj.spawn_time >= proj.life_time:
            cte_old.list_of_enemy_projectile.remove(proj)

        elif proj.collision(character, world_map):
            cte_old.list_of_enemy_projectile.remove(proj)


    #player projectiles
    for proj in cte_old.list_of_player_projectile.copy():
        proj.update()
        proj.draw_proj(cte_old.screen, bullet_rev, camera_move.camera_xy)

        remove_proj = False
        if current_time - proj.spawn_time >= proj.life_time:
            remove_proj = True
        elif not world_map.move_allowed((proj.x, proj.y), (proj.proj_area, proj.proj_area)):
            remove_proj = True

        else:
            for bot in cte_old.list_of_enemies.copy():
                if proj.collision(bot, world_map):
                    remove_proj = True
                    if bot.hp <= 0:
                        cte_old.list_of_enemies.remove(bot)

                    break

        if remove_proj:
            cte_old.list_of_player_projectile.remove(proj)
    
    #gunss
    for gun in cte_old.list_of_guns:
        pos_mouse_real = (pos_mouse[0] + camera_move.camera_xy[0], pos_mouse[1] + camera_move.camera_xy[1])
        gun.update_mouse_pos(pos_mouse_real)
        gun.rotate_gun(cte_old.orbit_xy[0], cte_old.orbit_xy[1], center_char_real)
        gun.draw_gun(cte_old.screen, gun.gun_surf, gun.rot_gun_screen, camera_move.camera_xy)

        if mouse_clicked:
            mouse_click = pos_mouse_real
            gun.shoot(current_time, mouse_click)

    pygame.display.update()
    clock.tick(cte_old.fps)

pygame.quit()