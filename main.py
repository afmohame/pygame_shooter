import pygame
import power_ups
import weapon
import characters
import collision
import cte
import world
pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
    
class Player(characters.Character):
    def __init__(self, pos, char_stat, hitbox_info, sprite_info, sprite_sheet, 
                 animation_info, animation_moves, power_up = (None, None)):
        super().__init__(pos, char_stat, hitbox_info, sprite_info, sprite_sheet, animation_info)
        self.stamina = char_stat["stamina"]
        self.animation_moves = animation_moves
        self.power_up1 = power_up[0]
        self.power_up2 = power_up[1]
    
    def moving(self):
        keys = pygame.key.get_pressed()

        self.column_index = self.animation_moves["idle"] #column index for resting sprite
        if keys[pygame.K_LSHIFT]:
            self.speed = 6
            #self.stamina -= 1
        else:
            self.speed = 4
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if world_map.move_allowed((self.x, self.y - self.speed), (self.hitbox_width, self.hitbox_height)):
                self.column_index = self.animation_moves["up"]
                self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
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

    def toggle_powerups(self):
        pass

class Enemies(characters.Character):
    def __init__(self, hp, defense, speed):
        #super().__init__(hp, defense, speed)
        pass

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
screen = pygame.display.set_mode((cte.screen_w, cte.screen_h))

#sprites
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 

# player
player = Player(
    cte.pos, cte.char_stat, cte.hitbox_info, cte.sprite_info, sprite_player, cte.animation_info, cte.animation_moves, (None, None))

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
run = True

shoot = False
map_generate = True
while run:
    screen.fill(cte.bg) #can't be deleted it refreshes the screen.

    #this block needs to be above other event.type otherwise it does not work 
    #repeating for event in pygame.event.get() is also not good
    #for loop does not create a local variable!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #draw world
    world_map.draw_world(screen, (camera_move.camera_x, camera_move.camera_y))

    pos_mouse = pygame.mouse.get_pos()
    #update animation
    current_time = pygame.time.get_ticks()#for animation tracks time passed
    if current_time - cte.last_update >= cte.animation_cooldown:
        cte.frame += 1
        cte.last_update = current_time
        if cte.frame >= 6:#len(animation_list):
            cte.frame = 0

    for character in cte.list_of_players:
        #camera
        camera_move.update_camera((cte.screen_w, cte.screen_h), (character.x, character.y), cte.sprite_w_h, cte.world_dim, cte.tile_size[0])
        character.draw_hitbox(screen, camera_move.camera_xy)#draws a hitbox in red
        character.moving()
        character.make_animation(cte.black, cte.first_x, cte.first_y, cte.x_space, cte.y_space, cte.column_length)
        character.draw_char(screen, character.get_animation(cte.frame), character.x, character.y, camera_move.camera_xy)#puts character on screen which is a surface
        center_char_real = (character.x + cte.sprite_info["sprite_player_width"]*cte.scale/2, 
                       character.y + cte.scale*cte.sprite_info["sprite_player_height"]/2)
        #character.update()

    for gun in cte.list_of_guns:
        pos_mouse_real = (pos_mouse[0] + camera_move.camera_xy[0], pos_mouse[1] + camera_move.camera_xy[1])
        gun.update_mouse_pos(pos_mouse_real)
        gun.rotate_gun(cte.orbit_xy[0], cte.orbit_xy[1], center_char_real)
        gun.draw_gun(screen, gun.gun_surf, gun.rot_gun_screen, camera_move.camera_xy)
        #gun.update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        shoot = True  
    if event.type == pygame.MOUSEBUTTONUP:
        shoot = False

    pygame.display.update()
    clock.tick(cte.fps)

pygame.quit()