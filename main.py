import pygame
import weapon
import characters
import cte
import world
import enemy
import projectile
pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
    
class Player(characters.Character):
    def __init__(self, pos, char_stat, hitbox_info, sprite_info, sprite_sheet, 
                 animation_info, animation_moves, frame, last_update, tile_size, power_up = (None, None)):
        super().__init__(pos, char_stat, hitbox_info, sprite_info, sprite_sheet, animation_info, frame, last_update)
        self.stamina = char_stat["stamina"]
        self.animation_moves = animation_moves
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]
        self.speedier = True
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)
        self.tile_size = tile_size
        self.tile_pos = (int(self.center[0]//tile_size), int(self.center[1]//tile_size))
    
    def update_tile_pos(self):
        self.center = (self.x + self.hitbox_width//2, self.y + self.hitbox_height//2)

        self.tile_pos = (int(self.center[0]//self.tile_size), int(self.center[1]//self.tile_size))

    def moving(self):
        keys = pygame.key.get_pressed()
        self.column_index = self.animation_moves["idle"] #column index for resting sprite

    # regenerate stamina when not holding shift
        if not keys[pygame.K_LSHIFT] and self.stamina < 10:
            self.stamina += 1

    # enable sprint again when stamina is full
        if self.stamina >= 100:
            self.speedier = True
            self.stamina = 100

    # disable sprint when stamina is empty
        if self.stamina <= 0:
            self.speedier = False
            self.stamina = 0

    # sprinting
        if keys[pygame.K_LSHIFT] and self.speedier:
            self.speed = 6
            self.stamina -= 1

        if keys[pygame.K_LSHIFT] and self.speedier:
            self.speed = 6
            self.stamina -= 1


        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if world_map.move_allowed((self.x - self.speed, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["up"]
                    self.x -= self.speed_xy
                    self.y -= self.speed_xy
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if world_map.move_allowed((self.x + self.speed, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["up"]
                    self.x += self.speed_xy
                    self.y -= self.speed_xy
            if world_map.move_allowed((self.x, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["up"]
                self.y -= self.speed

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if world_map.move_allowed((self.x - self.speed, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["down"]
                    self.x -= self.speed_xy
                    self.y += self.speed_xy
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if world_map.move_allowed((self.x + self.speed, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                    self.column_index = self.animation_moves["down"]
                    self.x += self.speed_xy
                    self.y += self.speed_xy
            if world_map.move_allowed((self.x, self.y + self.speed), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["down"]
                self.y += self.speed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if world_map.move_allowed((self.x - self.speed, self.y), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["left"]
                self.x -= self.speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if world_map.move_allowed((self.x + self.speed, self.y), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["right"]
                self.x += self.speed

        self.update_tile_pos()

    def toggle_powerups(self):
        pass
    
    def alive(self):
        if self.hp <= 0:
            print(f"Player dead")
            return False
        return True
        
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

# screen
clock = pygame.time.Clock()

#sprites
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
sprite_bot1 = pygame.image.load("sprites/images_chosen_for_game/bot1_walking.png")

# player
player = Player(
    cte.pos, cte.char_stat, cte.hitbox_info, cte.sprite_info, sprite_player, cte.animation_info, cte.animation_moves_player, 
    cte.frame, cte.last_update_player, cte.tile_size[0], (None, None))

#enemy 
bot1 = enemy.Enemy(
    (100, 100), cte.bot1_stats, cte.bot1_hitbox_info, cte.bot1_sprite_info, sprite_bot1, cte.bot1_animation_info, cte.animation_moves_enemies,
    cte.frame, cte.last_update_bot1, cte.last_atk, cte.tile_size[0])

#gun
weapon_xy = (cte.sprite_info["sprite_player_width"]*cte.scale, cte.scale*cte.sprite_info["sprite_player_height"]/2)
artillery = {"revolver": weapon.Weapons(weapon_xy, 3, 10, "common", sprite_revolver, cte.radius, 2, cte.center, cte.revolver_speed)}

#world
floor = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/06_Dungeon_Tileset.png"), cte.tile_size)
outer_walls = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/Dungeon_Tileset/00_right_outer_wall.png"), cte.tile_size)
destr_wall = pygame.transform.scale(pygame.image.load("sprites/images_chosen_for_game/column_sprite.png"), cte.tile_size)
world_map = world.World(cte.world_dim, floor, destr_wall, outer_walls, cte.tile_size[0])
world_map.generate_world()

#camera
camera_move = Camera(cte.camera_pos)
#animation preload
#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
cte.list_of_players.append(player)
cte.list_of_guns.append(artillery["revolver"])
cte.list_of_enemies.append(bot1)
run = True

shoot = False
map_generate = True
while run:
    cte.screen.fill(cte.bg) #can't be deleted it refreshes the screen.

    #this block needs to be above other event.type otherwise it does not work 
    #repeating for event in pygame.event.get() is also not good
    #for loop does not create a local variable!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pos_mouse = pygame.mouse.get_pos()
    #update animation
    current_time = pygame.time.get_ticks()#for animation tracks time passed
    
    #PLAYER
    for character in cte.list_of_players:
        character.moving()
        #camera
        camera_move.update_camera((cte.screen_w, cte.screen_h), (character.x, character.y), cte.sprite_w_h, cte.world_dim, cte.tile_size[0])
        #draw world
        world_map.draw_world(cte.screen, (camera_move.camera_x, camera_move.camera_y))

        character.draw_hitbox(cte.screen, camera_move.camera_xy)#draws a hitbox in red
        character.make_animation(cte.black, cte.first_x, cte.first_y, cte.x_space, cte.y_space, cte.column_length)
        character.get_frame(current_time, cte.animation_cooldown)
        character.draw_char(cte.screen, character.get_animation(), character.x, character.y, camera_move.camera_xy)#puts character on screen which is a surface
        center_char_real = (character.x + cte.sprite_info["sprite_player_width"]*cte.scale/2, 
                       character.y + cte.scale*cte.sprite_info["sprite_player_height"]/2)
        #print(f"player tile pos: {character.tile_pos}")
    
    #ENEMIES
    for bot in cte.list_of_enemies:
        bot.update(character, world_map, current_time)
        if not character.alive():
            run = False
        bot.make_animation(cte.black, cte.bot1_fx, cte.bot1_fy, cte.bot1_x_space, cte.bot1_y_space, cte.bot1_column_length)
        bot.get_frame(current_time, cte.animation_cooldown)
        bot.draw_hitbox(cte.screen, camera_move.camera_xy)
        bot.draw_bot(cte.screen, bot.get_animation(), bot.x, bot.y, camera_move.camera_xy)
        #print(f"bot tile pos: {bot.tile_pos}")
    
    for proj in cte.list_of_projectile.copy():
        proj.update()
        proj.draw_proj(cte.screen, enemy.projectile_img, camera_move.camera_xy)
        if current_time - proj.spawn_time >= proj.life_time or proj.collision(character, world_map):
            cte.list_of_projectile.remove(proj)
    
    #GUNS
    for gun in cte.list_of_guns:
        pos_mouse_real = (pos_mouse[0] + camera_move.camera_xy[0], pos_mouse[1] + camera_move.camera_xy[1])
        gun.update_mouse_pos(pos_mouse_real)
        gun.rotate_gun(cte.orbit_xy[0], cte.orbit_xy[1], center_char_real)
        gun.draw_gun(cte.screen, gun.gun_surf, gun.rot_gun_screen, camera_move.camera_xy)
        #gun.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        shoot = True
        #gun.shoot(bullet_image)
    if event.type == pygame.MOUSEBUTTONUP:
        shoot = False

    pygame.display.update()
    clock.tick(cte.fps)

pygame.quit()