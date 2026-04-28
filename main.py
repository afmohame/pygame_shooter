import pygame
import spritesheet
import power_ups
import weapon

pygame.init()
#-----------------------------------------------
#                   KLASSEN
#-----------------------------------------------
class Position():
    def __init__(self, x, y):
        self.x, self.y = x, y

class Collisions():
    def __init__(self):
        pass

class Character(Position):
    def __init__(self, pos, char_stat, hitbox_info, sprite_info, sprite_sheet, 
                 animation_info):
        super().__init__(pos[0], pos[1])
        self.sprite_sheet = spritesheet.Sprites(sprite_sheet)
        self.hp = char_stat["hp"]
        self.defense = char_stat["defense"]
        self.speed = char_stat["speed"]
        self.hitbox_width = hitbox_info["hitbox_width"]
        self.hitbox_height = hitbox_info["hitbox_height"] 
        self.hitbox_color = hitbox_info["hitbox_color"]  #temporary
        self.sprite_player_width = sprite_info["sprite_player_width"] 
        self.sprite_player_height = sprite_info["sprite_player_height"]
        self.scale = animation_info["scale"]
        self.animation_steps = animation_info["animation_steps"]
        self.column_index = animation_info["column_index"]
        self.animation_seq = []
            
    def make_animation(self, transparancy_color, first_x, first_y, x_space, y_space, column_length):
        #0 is the frame I want to use, width/height is  the height of the sprites box, scale is multiplier to make it bigger
        self.animation_seq = self.sprite_sheet.animation(self.animation_steps, self.column_index, first_x, first_y, self.sprite_player_width, 
                                                         self.sprite_player_height, self.scale, transparancy_color, x_space, y_space, column_length)
    def get_animation(self, frame):
        self.length_animation_list = len(self.animation_seq) 
        return self.animation_seq[frame]
    
    def draw_char(self, surface, blit_image, x, y):
        surface.blit(blit_image, (x, y))

    def draw_hitbox(self, surface):
        pygame.draw.rect(surface, self.hitbox_color, rect=(self.x, self.y, (self.hitbox_width)*self.scale, 
                                                           (self.hitbox_height)*self.scale))
        
class Player(Character):
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

class Enemies(Character):
    def __init__(self, hp, defense, speed):
        #super().__init__(hp, defense, speed)
        pass

#-----------------------------------------------
#                  constants
#-----------------------------------------------
# screen
screen_w, screen_h = 1500, 900
fps = 60
black, bg = (0, 0, 0), (100, 100, 100)#grey
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_w, screen_h))

# sprite state
sprite_player = pygame.image.load("sprites/images_chosen_for_game/player.png").convert_alpha()
sprite_revolver = pygame.image.load("sprites/images_chosen_for_game/enemy1_gun.png").convert_alpha() 
last_update = pygame.time.get_ticks()
animation_cooldown = 100 #miliseconds
frame = 0 

#ANIMATIONS
animation_moves = {"idle": 0, "up": 5, "down": 3, "left": -4, "right": 4, "dead": 9}
column_index = 0
first_x, x_space = 2, 48
first_y, y_space = 0, 48
scale = 3
column_length = 255
#animation_steps = 6 bcs there are 6 sprites for each, major, animation
animation_info = {"scale": 3, "animation_steps": 6, "column_index": 0} 

# player
pos = (0, 0)
char_stat = {"hp": 30, "defense": 10, "speed": 5, "stamina": 10}
hitbox_info = {"hitbox_width": 40, "hitbox_height": 65, "hitbox_color": (255, 0, 0)}
sprite_info = {"sprite_player_width": 14, "sprite_player_height": 21} 
player = Player(
    pos, char_stat, hitbox_info, sprite_info, sprite_player, animation_info, animation_moves, (None, None))

#guns
center = (sprite_info["sprite_player_width"]/2, sprite_info["sprite_player_height"]/2)
radius = sprite_info["sprite_player_height"]/2
orbit_xy = (40, 0)
weapon_xy = (sprite_info["sprite_player_width"]*scale, scale*sprite_info["sprite_player_height"]/2)
artillery = {"revolver": weapon.Weapons(weapon_xy, 3, 10, "common", sprite_revolver, radius, 2, center)}

#OTHERS
list_of_players, list_of_enemies, list_of_guns = [], [], []

#animation preload

#-----------------------------------------------
#                MAIN GAME LOOP
#-----------------------------------------------
list_of_players.append(player)
list_of_guns.append(artillery["revolver"])
run = True

anchor_surface = pygame.Surface((radius, radius))
anchor_point = pygame.draw.circle(anchor_surface, (0, 0, 200), (radius/2, radius/2), radius/2)

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
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= 6:#len(animation_list):
            frame = 0

    for character in list_of_players:
        #character.draw(screen)#draws a hitbox in red
        character.moving()
        character.make_animation(black, first_x, first_y, x_space, y_space, column_length)
        character.draw_char(screen, character.get_animation(frame), character.x, character.y)#puts character on screen which is a surface
        center_char = (character.x + sprite_info["sprite_player_width"], 
                       character.y + scale*sprite_info["sprite_player_height"]/2)
    screen.blit(anchor_surface, (center_char[0], center_char[1]))
    for gun in list_of_guns:
        gun.update_mouse_pos(pos_mouse)
        gun.rotate_gun(orbit_xy[0], orbit_xy[1], center_char)
        gun.draw_gun(screen, gun.gun_surf, gun.rot_gun_screen)

    if event.type == pygame.MOUSEBUTTONUP:
        pass        
    if event.type == pygame.MOUSEBUTTONDOWN:
        pass  


    pygame.display.update()
    clock.tick(fps)

pygame.quit()