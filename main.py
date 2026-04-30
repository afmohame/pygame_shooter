import pygame
import power_ups
import weapon
import characters
import collision
import cte
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
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.column_index = self.animation_moves["up"]
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.column_index = self.animation_moves["down"]
            self.y += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.column_index = self.animation_moves["left"]
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.column_index = self.animation_moves["right"]
            self.x += self.speed

    def toggle_powerups(self):
        pass

class Enemies(characters.Character):
    def __init__(self, hp, defense, speed):
        #super().__init__(hp, defense, speed)
        pass


# screen
screen_w, screen_h = 1500, 900
fps = 60
black, bg = (0, 0, 0), (100, 100, 100)#grey
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_w, screen_h))

#sprites
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 

# player
player = Player(
    cte.pos, cte.char_stat, cte.hitbox_info, cte.sprite_info, sprite_player, cte.animation_info, cte.animation_moves, (None, None))

#draw
anchor_surface = pygame.Surface((cte.radius, cte.radius))
anchor_point = pygame.draw.circle(anchor_surface, (0, 0, 200), (cte.radius/2, cte.radius/2), cte.radius/2)

#gun
weapon_xy = (cte.sprite_info["sprite_player_width"]*cte.scale, cte.scale*cte.sprite_info["sprite_player_height"]/2)
artillery = {"revolver": weapon.Weapons(weapon_xy, 3, 10, "common", sprite_revolver, cte.radius, 2, cte.center)}

#animation preload
#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
cte.list_of_players.append(player)
cte.list_of_guns.append(artillery["revolver"])
run = True

shoot = False
while run:
    screen.fill(bg) #can't be deleted it refreshes the screen.

    #this block needs to be above other event.type otherwise it does not work 
    #repeating for event in pygame.event.get() is also not good
    #for loop does not create a local variable!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pos_mouse = pygame.mouse.get_pos()
    #update animation
    current_time = pygame.time.get_ticks()#for animation tracks time passed
    if current_time - cte.last_update >= cte.animation_cooldown:
        cte.frame += 1
        cte.last_update = current_time
        if cte.frame >= 6:#len(animation_list):
            cte.frame = 0

    for character in cte.list_of_players:
        #character.draw(screen)#draws a hitbox in red
        character.moving()
        character.make_animation(black, cte.first_x, cte.first_y, cte.x_space, cte.y_space, cte.column_length)
        character.draw_char(screen, character.get_animation(cte.frame), character.x, character.y)#puts character on screen which is a surface
        center_char = (character.x + cte.sprite_info["sprite_player_width"], 
                       character.y + cte.scale*cte.sprite_info["sprite_player_height"]/2)
        #character.update()
    screen.blit(anchor_surface, (center_char[0], center_char[1]))
    for gun in cte.list_of_guns:
        gun.update_mouse_pos(pos_mouse)
        gun.rotate_gun(cte.orbit_xy[0], cte.orbit_xy[1], center_char)
        gun.draw_gun(screen, gun.gun_surf, gun.rot_gun_screen)
        #gun.update()
      
    if event.type == pygame.MOUSEBUTTONDOWN:
        shoot = True  
    if event.type == pygame.MOUSEBUTTONUP:
        shoot = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()